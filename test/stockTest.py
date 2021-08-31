import time
import pandas as pd
import trading.collector.constant as cons
import trading.collector.stock_collector as sc
from trading.config.logger import logger


# 获取A股所有股票代码
# sc.save_stock_basic()

# 遍历获取A股所有股票历史行情数据
# 加载所有股票代码
basic = pd.read_csv(cons.stock_basic_file)
for code in basic['code']:
    try:
        sc.save_history_k_data(str(code).zfill(6), adjust='hfq')
        time.sleep(1)
    except BaseException as e:
        logger.error(e)

# 更新某个股票
# sc.save_history_k_data('601919', adjust='hfq')
