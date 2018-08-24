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

def initialize(context):
    print('initialize')


def process_initialize(context):
    print('process_initialize')


def before_trading_start(context):
    print('before_trading_start')


def handle_data(context):
    context.order(context.market, 'ethbtc', 1000, 100)

def handle_tick(context):
    context.order(context.market, 'ethbtc', 1000, 200)

def after_trading_end(context):
    print('after_trading_end')

def on_strategy_end(context):
    print('on_strategy_end')

def after_code_changed(context):
    print('after_code_changed')
