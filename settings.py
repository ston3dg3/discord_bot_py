import envReplacement
import pathlib
import logging
from logging.config import dictConfig

DISCORD_API_SECRET = envReplacement.discrod_api
WOLFRAM_API_ID = envReplacement.wolfram_api
GUILD_ID = envReplacement.guild_id_ikea
BASE_DIR = pathlib.Path(__file__).parent
CMDS_DIR = BASE_DIR / "cmds"
COGS_DIR = BASE_DIR / "cogs"
SLASH_DIR = BASE_DIR / "slashcmds"

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