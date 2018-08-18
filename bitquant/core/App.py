import logging
import time

from bitquant.core import Service
from bitquant.core import Events
from bitquant.core import Worker
from bitquant.core import Task

class App(object):
    def __init__(self, ctx, services, routes):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='log/app.log',
                            filemode='w')

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

        self.ctx = ctx

        self.routes = routes
        self.evt_mng = Events.EventMananger()

        self.services = services
        self.services['WorkerService'] = Worker.WorkerService(
            self.ctx, self.routes)

        self.servMgr = Service.ServiceMgr(self.ctx, services)

    def run(self):
        self.servMgr.start()

        logging.info("bitquant startup.")

    def stop(self):
        self.servMgr.stop()
        logging.info('bitquant shutdown')
    
    def pubTask(self, ctx, action, id, data):
        self.services['WorkerService'].pubTask(ctx, action, id, data)
