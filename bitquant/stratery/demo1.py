import time
from datetime import datetime
import numpy as np
import pandas as pd
from bitquant.api import bqdata
import matplotlib.pyplot as plt
from matplotlib.pylab import date2num
import mpl_finance as mpf
import talib

'''
运行时间
开盘前(9:00)运行:

run_monthly/run_weekly/run_daily中指定time='before_open'运行的函数
before_trading_start
盘中运行:

run_monthly/run_weekly/run_daily中在指定交易时间执行的函数, 执行时间为这分钟的第一秒. 例如: run_daily(func, '14:50') 会在每天的14:50:00(精确到秒)执行
[handle_data]
按日回测/模拟, 在9:30:00(精确到秒)运行, data为昨天的天数据
按分钟回测/模拟, 在每分钟的第一秒运行, 每天执行240次, 不包括11:30和15:00这两分钟, [data]是上一分钟的分钟数据. 例如: 当天第一次执行是在9:30:00, data是昨天14:59这一分钟的分钟数据, 当天最后一次执行是在14:59:00, [data]是14:58这一分钟的分钟数据.
收盘后(15:00后半小时内)运行:

run_monthly/run_weekly/run_daily中指定time='after_close'运行的函数
after_trading_end
同一个时间点, 总是先运行 run_XXX 指定的函数, 然后是 before_trading_start , handle_data 和 after_trading_end

注意:

run_XXX 指定的函数只能有一个参数 context, data 不再提供, 请使用 history等获取
[initialize] / [before_trading_start] / [after_trading_end] / [handle_data] 都是可选的, 如果不是必须的, 不要实现这些函数, 一个空函数会降低运行速度.
'''

# 第一部分：策略参数
start = '20160101'                                  # 回测起始时间
end = '20180101'                                    # 回测结束时间
#benchmark = 'HS300'                                # 策略参考标准
universe = ['huobi.ethusdt', 'huobi.btcusdt']       # 证券池
capital_base = 100000                               # 起始资金
freq = 'd'                                          # 用日线回测的策略

# 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易日，若freq = 'm'时间间隔为分钟
refresh_rate = 1                                # 每天调一次仓，即每个交易日都会运行handle_data函数

def initialize(context):
    print('initialize')


def process_initialize(context):
    print('process_initialize')


def before_trading_start(context):
    print('before_trading_start')


def handle_data(context):
    order(1000, 100)
    print('hadle_data')


def handle_tick(context):
    print('handle_tick')

def after_trading_end(context):
    print('after_trading_end')


def on_strategy_end(context):
    print('on_strategy_end')

def after_code_changed(context):
    print('after_code_changed')
