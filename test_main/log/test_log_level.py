import logging
logger = logging.getLogger(__name__)


def test_log_level():
    logger.debug('debug')
    logger.info('info')
    logger.warn('warn')
    logger.error('error')
