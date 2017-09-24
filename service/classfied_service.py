import service.data_service as dsvc
import logging
import logging.config
from utils import util
import threading
import time

today = util.get_today()
today_line = util.get_today_line()

yestoday = util.get_yestoday()
yestoday_line = util.get_yestoday_line()

tomorrow = util.get_tomorrow()
tomorrow_line = util.get_tomorrow_line()

logger = logging.getLogger(__name__)
