import os
import logging
import logging.config


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "generic": {
                "()": "logging.Formatter",
                "fmt": "[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "formatter": "generic",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"],
        },
        "loggers": {
            "httpx": {"handlers": [], "level": "CRITICAL", "propagate": False},
        },
    }
)

APP_NAME = "beetle"

TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL", "sqlite:beetle.sqlite3")},
    "apps": {
        APP_NAME: {
            "models": ["beetle.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "timezone": "Asia/Shanghai",
}

TASK_POLL_INTERVAL = 60
OPENLIST_HOST = os.environ["OPENLIST_HOST"]
OPENLIST_TOKEN = os.environ["OPENLIST_TOKEN"]
