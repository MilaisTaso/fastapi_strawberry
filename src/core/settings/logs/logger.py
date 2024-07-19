from logging import Logger, getLogger
from logging.config import dictConfig

import yaml

from src.core.settings.config import settings

DEFAULT_PATH = settings.LOG_CONFIG_PATH


def init_logger(filepath: str = DEFAULT_PATH) -> None:
    with open(filepath) as f:
        config = yaml.safe_load(f)
        dictConfig(config)


# loggerの設定はこちらを使う
def get_logger(name: str) -> Logger:
    return getLogger(name)
