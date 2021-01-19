import trading.collector.stock_collector as sc
import pandas as pd
import time
import datetime
import os

from trading.collector.constant import (stock_basic_file, stock_history_path,
                                        stock_tradedate_file)

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)


# 筛选后一个交易日
def get_next_tradedate(date):
    tf = pd.read_csv(stock_tradedate_file)
    tf['trade_date'] = pd.to_datetime(tf['trade_date'])
    tf.sort_values('trade_date')
    tf = tf[tf['trade_date'] > date]
    return pd.Timestamp(tf['trade_date'].values[0]).to_pydatetime()


# 更新某个股票的历史行情数据
def update_stock_history_k_data(code):
    file_name = os.path.join(stock_history_path, code + ".csv")
    exists = os.path.exists(file_name)
    start_date = '1990-01-01'
    if (exists):
        data = pd.read_csv(file_name)
        data.index = pd.DatetimeIndex(data['date'])
        data = data.sort_index(ascending=False)
        start_date = data['date'].values[0]
        sdt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        sdt = get_next_tradedate(sdt)
        # 下个交易日大于当天,说明还没到,不获取数据
        if (sdt.date() > datetime.datetime.today().date()):
            return
        start_date = (sdt + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    sc.save_history_k_data(code,
                           start_date=start_date,
                           adjustflag="2",
                           save_header=bool(1 - exists))


# 登录
sc.bao_stock_login()

# 获取A股所有股票代码
# sc.save_stock_basic()

# 遍历获取A股所有股票历史行情数据
# 加载所有股票代码
# basic = pd.read_csv(stock_basic_file)
# basic = basic[basic['status'] == 1]
# for code in basic['code']:
#     update_stock_history_k_data(code)
#     time.sleep(2)

# 更新某个股票
update_stock_history_k_data('sh000300')
# 退出
sc.bao_stock_logout()
