import threading
import time
import queue
import logging
import json
import uuid
from bitquant.db import mysql_db
from bitquant.core import service
from bitquant.core import events
from bitquant.core import worker
import importlib
from bitquant.core import context

class StrategyContext():
    def __init__(self, stype, strategy_id, market, uid, did=None, data=None, options=None):
        self.type = stype
        self.strategy_id = strategy_id
        self.market = market
        self._uid = uid
        self.did = did
        self.data = data
        self.options = options

    #按数量下单
    def order(self, market, symbol,  amount, price):
        db = mysql_db.Mysql()
        
        s_uuid = ''.join(str(uuid.uuid1()).split('-'))
        cur_time = time.time()
        action = 'buy'
        vol = amount

        if amount < 0:
            action ='sell'
            vol = 0-amount


        attrs = {
            'id': s_uuid,
            'uid': self._uid,
            'strategy_id': self.strategy_id,
            'market': market,
            'symbol': symbol,
            'time': '%d' % cur_time,
            'action': action,
            'status': '00',
            'price': '%G' % price,
            'vol': '%G' % vol,
            'amount': '%G' % (price*vol),
            'did': '%d' % self.did,
            'create_date': time.strftime("%Y%m%d",  time.localtime(cur_time)),
            'create_time': time.strftime("%Y%m%d%H%M%S",  time.localtime(cur_time)),
        }

        try:
            db._insertDic('tx', attrs)
            logging.info('order stategy[%s] market[%s]  symbol[%s] amount[%f] price[%s]' % (self.strategy_id, market, symbol, amount, price))
        
        except BaseException as ex:
            logging.error(ex)
       
        db.dispose()

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
