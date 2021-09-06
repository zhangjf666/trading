import os
import traceback
import pandas as pd
import trading.collector.constant as cons
import trading.collector.stock_collector as sc
from trading.config.logger import logger


# 获取A股所有股票代码
# sc.save_stock_basic()

# 遍历获取A股所有股票历史行情数据
# 加载所有股票代码
# basic = pd.read_csv(cons.stock_basic_file, dtype={'code': str})
# # basic = basic[101:200]
# for code in basic['code']:
#     s_code = str(code).zfill(6)
#     try:
#         sc.save_history_k_data(s_code, adjust='qfq')
#         logger.info(str(s_code) + ':采集成功')
#     except BaseException:
#         logger.error(str(s_code) + ':采集失败,原因:' + traceback.format_exc())
# logger.info('采集完成')

# 更新某个股票
# sc.save_history_k_data('000001', adjust='qfq')

# 每日更新所有股票K线(需要每天连续执行,不能间断)
sc.update_k_data_daliy()

# basic = pd.read_csv(cons.stock_basic_file, dtype={'code': str})
# for index in basic.index:
#     row = basic.loc[index, :]
#     s_code = row['code']
#     name = row['name']
#     try:
#         file_name = os.path.join(cons.stock_history_path, s_code + ".csv")
#         data = pd.read_csv(file_name)
#         data['代码'] = s_code
#         # data.insert(1, '代码', s_code)
#         # data.insert(2, '名称', name)
#         data.to_csv(os.path.join(cons.stock_history_path, s_code + ".csv"), encoding="utf-8", index=False)
#         logger.info(str(s_code) + ':采集成功')
#     except BaseException:
#         logger.error(str(s_code) + ':采集失败,原因:' + traceback.format_exc())
