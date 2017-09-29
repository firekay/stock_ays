# encoding: UTF-8

from models.model import *
import tushare as ts
import logging

logger = logging.getLogger(__name__)


def save_stock_basic():
    logger.info('Begin save stock basic.')
    try:
        data_df = ts.get_stock_basics()
        data_df['code'] = pd.Series(data_df.axes[0], index=data_df.index)
        data = data_df.values
        data_dicts = [{'code': row[15], 'name': row[0], 'industry': row[1], 'area': row[2], 'pe': row[3],
                       'outstanding': row[4], 'totals': row[5], 'totalAssets':row[6], 'liquidAssets':row[7],
                       'fixedAssets': row[8], 'reserved': row[9], 'reservedPerShare': row[10], 'eps': row[11],
                       'bvps': row[12], 'pb': row[13], 'timeToMarket': row[14], 'insert_date': today}
                      for row in data]
        StockBasic.insert_many(data_dicts).execute()
    except Exception:
        logger.exception('Get stock basic.')
    logger.info('End save stock basic.')
