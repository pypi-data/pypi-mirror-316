import json
import logging
import re
import time
from multiprocessing import Process, Manager, Value

import oslo_messaging
import sqlalchemy as sa
from oslo_db.sqlalchemy import enginefacade
from oslo_middleware.healthcheck import pluginbase

from openstack_health_middleware import opts

LOG = logging.getLogger(__name__)


class InfraHealthCheck(pluginbase.HealthcheckBaseExtension):
    """InfraHealthCheck healthcheck middleware plugin

    This plugin checks:
    - messaging functionality
    - database functionality

    Example of middleware configuration:

    .. code-block:: ini

      [filter:healthcheck]
      paste.filter_factory = oslo_middleware:Healthcheck.factory
      path = /healthcheck
      backends = infra_health
      messaging_timeout = 5
      database_timeout = 5
      # set to True to enable detailed output, False is the default
      detailed = False
    """

    class LocalEndpoint:
        """LocalEndpoint class to receive incoming messages sent by the healthcheck."""

        def __init__(self, notification_time):
            self.notification_time = notification_time
            self._message_received = False
            self._payload = {}

        @property
        def payload(self):
            return self._payload

        @property
        def message_received(self):
            return self._message_received

        def info(self, ctxt, publisher_id, event_type, payload, metadata):
            if payload is not None:
                if "notification_time" in payload:
                    if self.notification_time == payload["notification_time"]:
                        LOG.info("Received expected healthcheck notification")
                        self._payload = payload
                        self._message_received = True

            LOG.debug("notification received %s:%s" % (publisher_id, event_type))
            output = json.dumps(
                {
                    "payload": payload,
                    "publisher_id": publisher_id,
                    "event_type": event_type,
                },
                indent=4,
            )
            LOG.debug(output)

    def __init__(self, *args, **kwargs):
        super(InfraHealthCheck, self).__init__(*args, **kwargs)
        self.result_dict = {}
        self.oslo_conf.register_opts(opts.INFRA_HEALTH_OPTS, group="healthcheck")
        self.messaging_timeout = self._conf_get("messaging_timeout")
        self.database_timeout = self._conf_get("database_timeout")
        self.messaging_thread = None
        self.database_thread = None
        self.messaging_available = False
        self.database_available = False
        LOG.info("InfraHealthCheck plugin loaded")

    def perform_messaging_check(self, available, result, transport_url):
        """Perform messaging check

        This is done by starting a messaging server using the configuration
        from the current environment (oslo_config).
        A message is sent using a notifier and is awaited to be received before
        a defined timeout.

        Parameters:
            available (multiprocessing.Value): is set to 1 if messaging is available
            result (multiprocessing.Manager.dict): will be filled with result messages
            transport_url (multiprocessing.Manager.dict): will be set to the transport url which was used
        """

        available.value = 0
        result.clear()

        notification_time = time.time_ns()
        local_endpoint = InfraHealthCheck.LocalEndpoint(notification_time)

        try:
            sender_transport = oslo_messaging.get_notification_transport(self.oslo_conf)
            notifier_transport = oslo_messaging.get_notification_transport(
                self.oslo_conf
            )

            transport_url["url"] = self.oslo_conf["transport_url"]
            server = oslo_messaging.get_notification_listener(
                sender_transport,
                [oslo_messaging.Target(topic="healthcheck")],
                [local_endpoint],
                executor="threading",
            )

            LOG.debug("Starting messaging server")
            server.start()

            notifier = oslo_messaging.Notifier(
                notifier_transport,
                "healthcheck",
                driver="messaging",
                topics=["healthcheck"],
            )

            LOG.debug(f"Sending healthcheck message: {notification_time}")
            notifier.info(
                ctxt={},
                event_type="health_check.check_messaging",
                payload={"notification_time": notification_time},
            )

            # wait until message was received or timeout was hit
            timeout = 0
            while (
                timeout < self.messaging_timeout and not local_endpoint.message_received
            ):
                LOG.debug(
                    f"Waiting for healthcheck notification to be received via messaging,"
                    f" timeout: {timeout}/{self.messaging_timeout}s"
                )
                time.sleep(1.0)
                timeout = timeout + 1

            # cleanup
            LOG.debug("Cleaning up messaging")
            server.stop()
            server.wait()
            sender_transport.cleanup()
            notifier_transport.cleanup()

            result.update({"message_sent": {"notification_time": notification_time}})

            if local_endpoint.message_received:
                available.value = 1
                result.update(
                    {"result": "Notification successfully received via messaging"}
                )
            else:
                result.update(
                    {
                        "result": f"Notification timed out after {self.messaging_timeout} seconds"
                    }
                )
        except Exception as e:
            result.update({"result": "Exception while checking messaging: " + str(e)})

    def perform_db_check(self, available, result, database_connection):
        """Perform database check

        This is done by connecting to the database using the configuration
        from the current environment (oslo_config).
        Also, a simple "SELECT 1" is done to check if the database is healthy.

        Parameters:
            available (multiprocessing.Value): is set to 1 if database is available
            result (multiprocessing.Manager.dict): will be filled with result messages
            database_connection (multiprocessing.Manager.dict): will be set to the connection string which was used
        """
        available.value = 0
        result.clear()

        try:
            engine = enginefacade.reader.get_engine()
            database_connection["connection"] = enginefacade.cfg.CONF.get("database")[
                "connection"
            ]
            LOG.debug("Connecting to DB")
            connection = engine.connect()

            total = connection.execute(sa.text("SELECT 1"))
            total_int = total.scalar()
            if total_int == 1:
                available.value = 1
                result.update({"result": "Connection to database is ok"})
        except Exception as e:
            result.update(
                {"result": "Exception while connecting to database: " + str(e)}
            )

    def _mistify(self, text):
        return re.sub(r"//[^:]+:[^@]+", "//***:***", text)

    def healthcheck(self, server_port):
        self.result_dict = {}

        # due to timeout handling checks are executed using multiprocessing lib
        manager = Manager()

        messaging_available = Value("i", 0)
        messaging_result = manager.dict()
        messaging_transport_url = manager.dict()
        messaging_transport_url["url"] = "unknown transport url"

        database_available = Value("i", 0)
        database_result = manager.dict()
        database_connection = manager.dict()
        database_connection["connection"] = "unknown connection string"

        process_messaging = Process(
            target=self.perform_messaging_check,
            args=(messaging_available, messaging_result, messaging_transport_url),
        )
        process_database = Process(
            target=self.perform_db_check,
            args=(database_available, database_result, database_connection),
        )

        LOG.debug("Starting infra health checks")
        process_messaging.start()
        process_database.start()
        LOG.debug("Waiting for infra health checks")
        process_messaging.join(self.messaging_timeout)
        process_database.join(self.database_timeout)
        LOG.debug("Infra health checks finished")

        # if no results where received just assume a timeout
        if not messaging_result:
            self.result_dict.update(
                {
                    "messaging": {
                        "result": f"Notification timed out after {self.messaging_timeout} seconds"
                    }
                }
            )
        else:
            self.result_dict.update({"messaging": dict(messaging_result)})

        if not database_result:
            self.result_dict.update(
                {
                    "database": {
                        "result": f"Connection timed out after {self.database_timeout} seconds"
                    }
                }
            )
        else:
            self.result_dict.update({"database": dict(database_result)})

        transport_url = self._mistify(messaging_transport_url["url"])
        db_connection = self._mistify(database_connection["connection"])

        self.result_dict["messaging"].update({"transport_url": transport_url})
        self.result_dict["database"].update({"connection": db_connection})

        available = messaging_available.value == 1 and database_available.value == 1

        return pluginbase.HealthcheckResult(
            available=available, reason=[self.result_dict]
        )
