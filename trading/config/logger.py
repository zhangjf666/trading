import os
import time
import logging
import logging.config
import logging.handlers
import trading.util.file_util as fileUtil

cur_path = os.path.abspath('/python/data/trading/')  # log_path是存放日志的路径
log_path = os.path.join(cur_path, 'logs')
fileUtil.createPath(log_path)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        # 日志格式
        'standard': {
            'format': '[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] '
                      '[%(levelname)s]- %(message)s'},
        'simple': {  # 简单格式
            'format': '%(levelname)s %(message)s'
        },
    },
    # 过滤
    'filters': {
    },
    # 定义具体处理日志的方式
    'handlers': {
        # 控制台输出
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 默认记录所有日志
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(log_path, 'log.{}.log'.format(time.strftime('%Y-%m-%d'))),
            'when': 'midnight',  # 滚动时间
            'backupCount': 5,  # 备份数
            'interval': 1,
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        # 输出错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(log_path, 'error.{}.log'.format(time.strftime('%Y-%m-%d'))),
            'when': 'midnight',  # 滚动时间
            'backupCount': 5,  # 备份数
            'interval': 1,
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        }
    },
    'root': {
        'handlers': ['console', 'debug', 'error'],
        'level': 'INFO'
    }
    # 配置用哪几种 handlers 来处理日志
    # 'loggers': {
    #     # 类型 为 django 处理所有类型的日志， 默认调用
    #     'django': {
    #         'handlers': ['default', 'console'],
    #         'level': 'INFO',
    #         'propagate': False
    #     },
    #     # log 调用时需要当作参数传入
    #     'log': {
    #         'handlers': ['error', 'info', 'console', 'default'],
    #         'level': 'INFO',
    #         'propagate': True
    #     },
    # }
}

logging.config.dictConfig(LOGGING)

logger = logging
