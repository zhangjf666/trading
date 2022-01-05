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
    # 更新交易日信息
    sc.save_tradeday()
    # 股票基本信息
    sc.save_stock_basic()
    # 当日K线
    sc.update_k_data_daliy()
    # 北向资金
    sc.save_n2s()
    # 可转债比价表
    sc.update_convertible()
    # 均线多头选股策略
    ma_higher.select_stock_ma()
    # 超跌次新买入卖出策略
    oversoldNewStock.selectOversoldStock()
    oversoldNewStock.sellOverStock()


def update_board_task():
    # 板块指数相关
    sc.update_industry_board()
    sc.update_concept_board()
    sc.update_industry_stocks()
    sc.update_concept_stocks()
    sc.update_all_industry_index()
    sc.update_all_concept_index()
    # 指数均线策略
    ma_higher.select_board_index_ma('1')
    ma_higher.select_board_index_ma('2')


def update_index_task():
    # 指数更新相关
    sc.update_index()
    sc.update_index_daily()
    sc.update_index_stocks()


if __name__ == '__main__':
    # now = datetime.datetime(2021, 1, 1, 20, 0, 0)
    now = datetime.datetime.now()
    nexttime = now + datetime.timedelta(minutes=1)
    # 添加股票数据更新任务
    scheduler.add_job(update_stock_task, 'cron', day_of_week='*', hour=nexttime.hour, minute=nexttime.minute)
    # 添加板块数据更新任务
    nexttime = nexttime + datetime.timedelta(minutes=1)
    scheduler.add_job(update_board_task, 'cron', day_of_week='*', hour=nexttime.hour, minute=nexttime.minute)
    # 添加指数数据更新任务
    nexttime = nexttime + datetime.timedelta(minutes=1)
    scheduler.add_job(update_index_task, 'cron', day_of_week='*', hour=nexttime.hour, minute=nexttime.minute)

    try:
        # 开始调度
        scheduler.print_jobs()
        logger.info('计划任务开始')
        scheduler.start()
    except BaseException as e:
        scheduler.shutdown()
        logger.error('计划任务结束:' + e)
