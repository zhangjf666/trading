# 导入模块
import sys,os
sys.path.extend(['F:/python/envs/trading/Lib/site-packages'])
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import datetime
# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from trading.config.logger import logger
import trading.collector.stock_collector as sc

scheduler = BlockingScheduler()


def update_stock_basic():
    sc.save_stock_basic()


def update_k_data():
    sc.update_k_data_daliy()


def update_n2s():
    sc.save_n2s()


if __name__ == '__main__':
    now = datetime.datetime.now()
    # 添加获取所有股票代码任务
    nexttime = now + datetime.timedelta(minutes=1)
    scheduler.add_job(update_stock_basic, 'cron', day_of_week='*', hour=nexttime.hour, minute=nexttime.minute)
    # 添加更新北向资金任务
    nexttime = nexttime + datetime.timedelta(minutes=2)
    scheduler.add_job(update_stock_basic, 'cron', day_of_week='*', hour=nexttime.hour, minute=nexttime.minute)
    # 添加更新股票历史数据任务
    nexttime = nexttime + datetime.timedelta(minutes=5)
    scheduler.add_job(update_k_data, 'cron', day_of_week='*', hour=nexttime.hour, minute=nexttime.minute)
    try:
        # 开始调度
        scheduler.start()
        logger.info('计划任务开始')
    except BaseException as e:
        scheduler.shutdown()
        logger.error('计划任务结束:' + e)
