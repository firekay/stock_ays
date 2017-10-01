import logging.config
import os
import sys

import yaml

import test_log_level

reload(sys)
sys.setdefaultencoding('utf8')

def setup_logging(
    default_path='../resources/logging.yaml',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


if __name__ == '__main__':
    setup_logging()
    test_log_level.test_log_level()
