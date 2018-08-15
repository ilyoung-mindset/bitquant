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

from bitquant.ex_broker import EXBroker
from bitquant.ex_broker.huobi import HuobiWS
from bitquant.ex_broker.hadax import HadaxWS
from bitquant.ex_broker.lbank import LbankWS

from bitquant.rules import MarketInner
from bitquant.ex_broker import EXTradeWorker

routes = {
    'test': Worker.Router(),
    #'exbroker/huobi/ws/depth': MarketInner.Router({'fifo': True}),
    #'exbroker/hadax/ws/depth': MarketInner.Router({'fifo': True}),
    'exbroker/hadax/ws/trade': EXTradeWorker.Router(),
    #'exbroker/lbank/ws': EXTradeWorker.Router(),
}

ctx = {
    'params': Params.params
}

services = {
    'EXBrokerService': EXBroker.EXBrokerService(ctx),
    'HuobiWSService': HuobiWS.HuobiWSService(ctx),
    'HadaxWSService': HadaxWS.HadaxWSService(ctx),
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
