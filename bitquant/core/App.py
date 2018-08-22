import logging
import time

from bitquant.core import service
from bitquant.core import events
from bitquant.core import worker

class App(object):
    def __init__(self, ctx, services, routes):
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

        self.ctx = ctx

        self.routes = routes
        self.evt_mng = events.EventMananger()

        self.services = services
        self.services['WorkerService'] = worker.WorkerService(
            self.ctx, self.routes)

        self.servMgr = service.ServiceMgr(self.ctx, services)

    def run(self):
        self.servMgr.start()

        logging.info("bitquant startup.")

    def stop(self):
        self.servMgr.stop()
        logging.info('bitquant shutdown')
    
    def pubTask(self, ctx, action, id, data):
        self.services['WorkerService'].pub_task(ctx, action, id, data)
