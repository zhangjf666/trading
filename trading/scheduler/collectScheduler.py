# 导入模块
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from trading.config.logger import logger
import trading.collector.stock_collector as sc
from trading.strategy import ma_higher, oversoldNewStock

scheduler = BlockingScheduler()


def update_stock_task():
    if not (sc.is_trade_date(datetime.datetime.today().strftime('%Y-%m-%d'))):
        logger.warning('非交易日,不进行更新.')
        return
    # 股票基本信息
    sc.save_stock_basic()
    # 当日K线
    sc.update_k_data_daliy()
    # 北向资金
    sc.save_n2s()
    # 均线多头选股策略
    ma_higher.select_ma_higher()
    # 超跌次新买入卖出策略
    oversoldNewStock.selectOversoldStock()
    oversoldNewStock.sellOverStock()


def update_board_task():
    if not (sc.is_trade_date(datetime.datetime.today().strftime('%Y-%m-%d'))):
        logger.warning('非交易日,不进行更新.')
        return
    sc.update_industry_board()
    sc.update_concept_board()


if __name__ == '__main__':
    # now = datetime.datetime(2021, 1, 1, 20, 0, 0)
    now = datetime.datetime.now()
    nexttime = now + datetime.timedelta(minutes=1)
    # 添加股票数据更新任务
    scheduler.add_job(update_stock_task, 'cron', day_of_week='*', hour=nexttime.hour, minute=nexttime.minute)
    # 添加板块数据更新任务
    scheduler.add_job(update_board_task, 'cron', day_of_week='*', hour=nexttime.hour, minute=nexttime.minute)

    try:
        # 开始调度
        scheduler.print_jobs()
        logger.info('计划任务开始')
        scheduler.start()
    except BaseException as e:
        scheduler.shutdown()
        logger.error('计划任务结束:' + e)
