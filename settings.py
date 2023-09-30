from dotenv import load_dotenv
import os
import logging
from logging.config import dictConfig

load_dotenv()

DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
WOLFRAM_API_ID = os.getenv("WOLFRAM_API_ID")

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_Loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {
            "format": "%(levelname)-10s - %(name)-15s : %(message)s"
        }
    },
    "handlers":{
        "console": {
            'level': "DEBUG",
            'class': "logging.StreamHandler",
            'formatter': "standard",
        },
        "console2": {
            'level': "WARNING",
            'class': "logging.StreamHandler",
            'formatter': "standard",
        },
        "file": {
            'level': "INFO",
            'class': "logging.FileHandler",
            'formatter': "verbose",
            'filename': "logs/infos.log",
            'mode': "w"
        }
    },
    "loggers":{
        "bot": {
            'handlers': ['console'],
            'level': "INFO",
            "propagate": False
        },
        "discord": {
            'handlers': ['console2','file'],
            'level': "INFO",
            "propagate": False
        }
    }
}