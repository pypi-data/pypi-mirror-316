from oslo_config import cfg

INFRA_HEALTH_OPTS = [
    cfg.IntOpt(
        "messaging_timeout",
        default=5,
        help="Timeout in seconds for test notification to be received.",
    ),
    cfg.IntOpt(
        "database_timeout",
        default=5,
        help="Timeout in seconds for database connection to succeed.",
    ),
]
