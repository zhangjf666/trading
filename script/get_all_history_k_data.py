# -*- coding:utf-8 -*-
"""
Date: 2021-01-14 22:00:56
Desc: 获取所有A股历史日K线脚本
"""
import traceback
import pandas as pd
import trading.collector.constant as cons
import trading.collector.stock_collector as sc
from trading.config.logger import logger


if __name__ == '__main__':
    basic = pd.read_csv(cons.stock_basic_file, dtype={'代码': str})
    for index in basic.index:
        row = basic.loc[index, :]
        s_code = row['代码']
        name = row['名称']
        try:
            sc.save_history_k_data(s_code, name)
            logger.info(str(s_code) + ':采集成功')
        except BaseException:
            logger.error(str(s_code) + ':采集失败,原因:' + traceback.format_exc())
    logger.info('采集完成')
