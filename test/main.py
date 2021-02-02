import numpy as np
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import os
import sys
import akshare as ak

from trading.collector.constant import (stock_basic_file, stock_history_path,
                                        stock_tradedate_file, stock_n2s_path)


df = ak.stock_em_yjyg(date="2020-12-31")
print(df)
