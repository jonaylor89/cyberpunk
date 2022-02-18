class LoggerConfig:
    dictConfig = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - "
                "%(message)s - [in %(pathname)s:%(lineno)d]",
            },
            "short": {"format": "%(message)s"},
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
            },
            "debug": {
                "level": "DEBUG",
                "formatter": "standard",
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "cyberpunk": {
                "handlers": ["default"],
                "level": "DEBUG",
                "propagate": True,
            },
            "werkzeug": {"propagate": True},
        },
        # 'root': { 'level': 'DEBUG', 'handlers': ['console'] }
    }
