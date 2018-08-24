import threading
import time
import queue
import logging
import json
import pymysql.cursors
from bitquant.core import service
from bitquant.core import events
from bitquant.core import worker
import importlib
from bitquant.core import context

class StrategyContext():
    def __init__(self, stype, market, uid, did=None, data=None, options=None):
        self.type = stype
        self.market = market
        self._uid = uid
        self.did = did
        self.data = data
        self.options = options

    #按数量下单
    def order(self, market, symbol,  amount, price):
        logging.info('order market[%s]  symbol[%s] amount[%f] price[%s]' %
                     (market, symbol, amount, price))

    #目标股数下单
    def order_target(self, market, symbol):
        pass

    #按价值下单
    def order_value(self, market, symbol):
        pass

    #目标价值下单
    def order_target_value(self, market, symbol):
        pass

    #撤单
    def cancel_order(self, market, symbol):
        pass

    #获取未完成订单
    def get_open_orders(self, market, symbol):
        pass

    #获取订单信息
    def get_orders(self, market, symbol):
        pass

    #获取成交信息
    def get_trades(self, market, symbol):
        pass

    #账户出入金
    def inout_cash(self, market, symbol):
        pass

    #获取历史数据
    def get_current_data(self):
        pass
