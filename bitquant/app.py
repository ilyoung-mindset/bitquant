#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import threading
import time
import signal
import logging
import optparse

from bitquant.db import mysql_db 
from bitquant.core import worker

from bitquant.core import application
from bitquant.core import context
from bitquant.params import Params

from bitquant.ex_broker import ex_broker_service
from bitquant.ex_broker.huobi import huobi_service
from bitquant.ex_broker.hadax import hadax_service
from bitquant.ex_broker.lbank import lbank_service

from bitquant.rules import inner_market_tick
from bitquant.ex_broker import market_trade_worker
from bitquant.ex_broker import market_kline_woker
from bitquant.ex_broker import market_depth_worker

from bitquant.strategy import strategy_service
from bitquant.strategy import strategy_worker

mysql_db._init(Params.params['db'])

context._init()

routes = {
    'exbroker/huobi/ws/depth': worker.Router(market_depth_worker.EXDepthWorker),
    'exbroker/huobi/ws/kline': worker.Router(market_kline_woker.EXMarketWorker),
    'exbroker/huobi/rest/kline': worker.Router(market_kline_woker.EXMarketWorker),
    'exbroker/hadax/ws/depth': worker.Router(market_depth_worker.EXDepthWorker),
    'exbroker/hadax/ws/kline': worker.Router(market_kline_woker.EXMarketWorker),
    'exbroker/hadax/ws/trade': worker.Router(market_trade_worker.EXTradeWorker),
    'exbroker/hadax/rest/kline': worker.Router(market_kline_woker.EXMarketWorker),
    
    #'exbroker/lbank/ws': worker.Router(market_trade_worker.EXTradeWorker),

    'exbroker/hadax/ws/depth': worker.Router(inner_market_tick.MarketInnerWorker, {'fifo': True}),

    'exbroker/kline/tick': worker.Router(strategy_worker.StrategyTickWorker),

    'strategy/tick': worker.Router(strategy_worker.StrategyWorker),
    'strategy/min': worker.Router(strategy_worker.StrategyWorker),
    'strategy/day': worker.Router(strategy_worker.StrategyWorker),
}

ctx = context.get_context()
ctx['params'] = Params.params

services = {
    'HuobiService': huobi_service.HuobiService(ctx, Params.paramsHuobi.params),
    'HadaxService': hadax_service.HadaxService(ctx, Params.paramsHadax.params),
    #'LbankWSService': lbank_service.LbankWSService(ctx),
    'EXBrokerService': ex_broker_service.EXBrokerService(ctx),
    'StrategyService': strategy_service.StrategyService(ctx),
}

app = application.Application(ctx, services, routes)

ctx['app'] = app

def appQuit(signum, frame):
    logging.warning('receive signal SIGTERM')
    app.stop()
    
if __name__ == "__main__":
    parse = optparse.OptionParser( usage='"usage:%prog [options]"', version="%prog 0.1")
    parse.add_option('-d', dest='daemon', action='store_true', metavar='daemon', help='bitquant run as daemon ')
    parse.add_option('-v', help='bitquant 0.1')
    parse.set_defaults(v=0.1)

    options, args = parse.parse_args()

    signal.signal(signal.SIGTERM, appQuit)
  
    app.run()
