import traceback
import pandas as pd
import trading.collector.constant as cons
import trading.collector.stock_collector as sc
from trading.config.logger import logger


# 获取A股所有股票代码
# sc.save_stock_basic()

# 遍历获取A股所有股票历史行情数据
# 加载所有股票代码
basic = pd.read_csv(cons.stock_basic_file, dtype={'code': str})
basic = basic[3019:3048]
for code in basic['code']:
    s_code = str(code).zfill(6)
    try:
        sc.save_history_k_data(s_code, adjust='qfq')
        logger.info(str(s_code) + ':采集成功')
    except BaseException:
        logger.error(str(s_code) + ':采集失败,原因:' + traceback.format_exc())

# 更新某个股票
# sc.save_history_k_data('000001', adjust='qfq')
