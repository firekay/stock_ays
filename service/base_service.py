# encoding: UTF-8
""""""

import logging
from utils.mysql_utils import *
from models.model import *

logger = logging.getLogger(__name__)


# @conn
def save_stocks_basic_data():
    data_df = ts.get_stock_basics()
    data_df['code'] = pd.Series(data_df.axes[0], index=data_df.index)
    data = data_df.values
    # logger.debug(data)
    data_dicts = [{'code': row[22], 'name': row[0], 'industry': row[1], 'area': row[2], 'pe': row[3],
                   'outstanding': row[4], 'totals': row[5], 'totalAssets':row[6], 'liquidAssets':row[7],
                   'fixedAssets': row[8], 'reserved': row[9], 'reservedPerShare': row[10], 'eps': row[11],
                   'bvps': row[12], 'pb': row[13], 'timeToMarket': row[14], 'undp': row[15],
                   'perundp': row[16], 'rev': row[17], 'profit': row[18], 'gpr': row[19], 'npr': row[20],
                   'holders': row[21], 'insert_date': today} for row in data]
    StockBasic.insert_many(data_dicts).execute()
