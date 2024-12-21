# openstack-health-middleware

This middleware checks the healthiness of an OpenStack component by checking its
configured database and messaging services (e.g. MariaDB and RabbitMQ).

In the future more checks, like e.g. log file checking will be implemented.

This plugin is derived from the official `oslo.middleware` 
[healthcheck](https://docs.openstack.org/oslo.middleware/latest/reference/healthcheck_plugins.html)
and should behave as described in that document:

- it returns HTTP status code 200 if infrastructure checks were successful
- it returns HTTP status code 503 if at least one check was not successful

## Configuration

The plugin can be enabled via the `api-paste.ini` under the `[app:healthcheck]` group.

See this example configuration for neutron `api-paste.ini`:

```
[composite:neutron]
use = egg:Paste#urlmap
/networking/: neutronversions_composite
/networking/healthcheck: healthcheck
/networking/v2.0: neutronapi_v2_0

...

[app:healthcheck]
paste.app_factory = oslo_middleware:Healthcheck.app_factory
oslo_config_project = neutron
backends = infra_health
messaging_timeout = 5
database_timeout = 5
detailed = False
```

### Options

`messaging_timeout`: Timeout in seconds for test notification to be received.

`database_timeout`: Timeout in seconds for database connection to succeed.

## Usage

The check itself can be executed by calling the `healthcheck` endpoint of
the respective OpensStack component, e.g. neutron:

```
curl -X GET -i -H "Accept: application/json" http://192.168.13.37:9696/networking/healthcheck

HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 650
Date: Wed, 14 Aug 2024 08:38:55 GMT

{
    "detailed": false,
    "reasons": [
        [
            {
                "database": {
                    "connection": "mysql+pymysql://***:***@127.0.0.1/neutron?charset=utf8&plugin=dbcounter",
                    "result": "Connection to database is ok"
                },
                "messaging": {
                    "message_sent": {
                        "notification_time": 1723624734622068313
                    },
                    "result": "Notification successfully received via messaging",
                    "transport_url": "rabbit://***:***@192.168.13.37:5672/"
                }
            }
        ]
    ]
}
```

This example shows a result with unavailable status:

```
curl -X GET -i -H "Accept: application/json" http://192.168.13.37:9696/networking/healthcheck
HTTP/1.1 503 Service Unavailable
Content-Type: application/json
Content-Length: 514
Date: Wed, 14 Aug 2024 08:56:02 GMT

{
    "detailed": false,
    "reasons": [
        [
            {
                "database": {
                    "connection": "mysql+pymysql://***:***@127.0.0.1/neutron?charset=utf8&plugin=dbcounter",
                    "result": "Connection to database is ok"
                },
                "messaging": {
                    "result": "Notification timed out after 5 seconds",
                    "transport_url": "rabbit://***:***@192.168.13.37:5672/"
                }
            }
        ]
    ]
}
```

## Future ideas

- check processes like nova-compute if they are running (e.g. because logs stopped being written)
- check the logs for errors
