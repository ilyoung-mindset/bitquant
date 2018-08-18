#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import threading
import time
import signal
import logging
import optparse
from daemon.runner import DaemonRunner

from bitquant.core import Service
from bitquant.core import Events
from bitquant.core import Worker

from bitquant.core import Task
from bitquant.core import App
from bitquant.params import Params

from bitquant.ex_broker import ex_broker_service
from bitquant.ex_broker.huobi import huobi_service
from bitquant.ex_broker.hadax import hadax_service
from bitquant.ex_broker.lbank import LbankWS

from bitquant.rules import MarketInner
from bitquant.ex_broker import EXTradeWorker
from bitquant.ex_broker import EXMarketWorker
from bitquant.ex_broker import EXDepthWorker

routes = {
    'test': Worker.Router(),
    'exbroker/huobi/ws/depth': EXDepthWorker.Router(),
    'exbroker/huobi/ws/kline': EXMarketWorker.Router(),

    'exbroker/hadax/ws/depth': EXDepthWorker.Router(),
    'exbroker/hadax/ws/kline': EXMarketWorker.Router(),
    'exbroker/hadax/ws/trade': EXTradeWorker.Router(),
    
    #'exbroker/lbank/ws': EXTradeWorker.Router(),

    'exbroker/hadax/ws/depth': MarketInner.Router({'fifo': True}),
}

ctx = {
    'params': Params.params
}

services = {
    'EXBrokerService': ex_broker_service.EXBrokerService(ctx),
    'HuobiWSService': huobi_service.HuobiWSService(ctx, Params.paramsHuobi.params),
    'HadaxWSService': hadax_service.HadaxWSService(ctx, Params.paramsHadax.params),
    #'LbankWSService': LbankWS.LbankWSService(ctx),
}

app = App.App(ctx, services, routes)

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

    if options.daemon:
        print("run as daemon")
        run = DaemonRunner(app)
        run.do_action()
    else:
        app.run()
