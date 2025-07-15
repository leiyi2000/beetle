import os
import logging

APP_NAME = "beetle"

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "generic": {
                "()": "logging.Formatter",
                "fmt": "[%(levelname)s] %(pathname)s:%(lineno)d - %(message)s",
                "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
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
    }
)

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

SYNCHRONIZER_COUNT = 5
TASK_POLL_INTERVAL = 60
OPENLIST_HOST = os.environ["OPENLIST_HOST"]
OPENLIST_TOKEN = os.environ["OPENLIST_TOKEN"]
