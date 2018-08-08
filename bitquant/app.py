#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import time
import logging
import optparse
from daemon.runner import DaemonRunner

from bitquant.core import Service
from bitquant.ex_broker import EXBroker


class App(object):
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='log/app.log',
                            filemode='w')

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    def run(self):
        service = EXBroker.EXBrokerService()
        service.start()

        logging.info("bitquant startup.")

        for num in range(1, 5):
            task = Service.Task('data', str(num), "task:"+str(num))
            service.workQuque.put(task)
            time.sleep(1)

        service.stop()
        logging.warning('bitquant shutdown')

if __name__ == "__main__":
    parse = optparse.OptionParser( usage='"usage:%prog [options]"', version="%prog 0.1")
    parse.add_option('-d', dest='daemon', action='store_true', metavar='daemon', help='bitquant run as daemon ')
    parse.add_option('-v', help='bitquant 0.1')
    parse.set_defaults(v=0.1)

    options, args = parse.parse_args()

    app = App()

    if options.daemon:
        print("run as daemon")
        run = DaemonRunner(app)
        run.do_action()
    else:
        app.run()
