# 导入模块
from logging import log
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from trading.config.logger import logger
import trading.collector.stock_collector as sc
from trading.strategy import ma_higher, oversoldNewStock

scheduler = BlockingScheduler()


# 交易日任务
def tradeday_task():
    # 更新交易日信息
    sc.save_tradeday()
    if not sc.is_trade_date(datetime.datetime.today().strftime('%Y-%m-%d')):
        logger.info('非交易日,不进行采集')
        return
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

    # 板块指数相关
    sc.update_industry_board()
    sc.update_concept_board()
    sc.update_all_industry_index()
    sc.update_all_concept_index()
    # 指数均线策略
    ma_higher.select_board_index_ma('1')
    ma_higher.select_board_index_ma('2')

    # 指数更新相关
    sc.update_index()
    sc.update_index_daily()

    # 技术指标
    sc.update_cxg_daily()
    sc.update_cxd_daily()
    sc.update_lxsz_daily()
    sc.update_lxxd_daily()
    sc.update_cxfl_daily()
    sc.update_cxsl_daily()
    sc.update_ljqs_daily()
    sc.update_ljqd_daily()
    # 资金排行
    sc.update_ggzj_daily(symbol='当日排行')
    sc.update_ggzj_daily(symbol='3日排行')
    sc.update_ggzj_daily(symbol='5日排行')
    sc.update_ggzj_daily(symbol='10日排行')
    sc.update_ggzj_daily(symbol='20日排行')
    sc.update_gnzj_daily(symbol='当日排行')
    sc.update_gnzj_daily(symbol='3日排行')
    sc.update_gnzj_daily(symbol='5日排行')
    sc.update_gnzj_daily(symbol='10日排行')
    sc.update_gnzj_daily(symbol='20日排行')
    sc.update_hyzj_daily(symbol='当日排行')
    sc.update_hyzj_daily(symbol='3日排行')
    sc.update_hyzj_daily(symbol='5日排行')
    sc.update_hyzj_daily(symbol='10日排行')
    sc.update_hyzj_daily(symbol='20日排行')


# 日频任务
def daily_task():
    # 机构调研
    sc.update_jgdy_tj()
    # 研究报告
    sc.update_yjbg()


# 周频任务
def weekly_task():
    # 板块相关
    sc.update_industry_stocks()
    sc.update_concept_stocks()

    # 指数相关
    sc.update_index_stocks()


if __name__ == '__main__':
    # now = datetime.datetime(2021, 1, 1, 20, 0, 0)
    now = datetime.datetime.now()
    nexttime = now + datetime.timedelta(minutes=1)
    # 日频任务
    scheduler.add_job(tradeday_task, 'cron', day_of_week='*', hour=nexttime.hour, minute=nexttime.minute)
    scheduler.add_job(daily_task, 'cron', day_of_week='*', hour=nexttime.hour, minute=nexttime.minute)
    # 周频任务
    scheduler.add_job(weekly_task, 'cron', day_of_week='mon', hour=20, minute=0)

    try:
        # 开始调度
        scheduler.print_jobs()
        logger.info('计划任务开始')
        scheduler.start()
    except BaseException as e:
        scheduler.shutdown()
        logger.error('计划任务结束:' + e)
