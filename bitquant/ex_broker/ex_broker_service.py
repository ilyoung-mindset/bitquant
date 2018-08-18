import threading
import time
import queue
import logging
from bitquant.core import Service
from bitquant.core import Events


'''
Market data API
'''


class WorkerThread(threading.Thread):
    def __init__(self, q, service):
        threading.Thread.__init__(self)
        self.service = service
        # 初始化
        self.taskQueue = q

    def run(self):

        while True:
            worker = self.taskQueue.get()

            if worker.task.action == 'quit':
                break

class EXBrokerService(Service.Service):
    def __init__(self, ctx):
        Service.Service.__init__(self, ctx, "EXBroker", EventProccess)
        self.eventHandler = EventProccess
        self.taskQueue = queue.Queue()
        self.workThread = WorkerThread(self.taskQueue, self)

    def after_start(self):
        ev = Events.Event('market.huobi.get', str(1), {'symbol': 'ethusdt', 'period': '1day', 'size':2000})
        self.ctx['app'].evt_mng.pub_event(ev)
        

def EventProccess(e, service=None):
    logging.debug(e.data)
  

if __name__ == "__main__":
    service = EXBrokerService(None)
    service.start()

    for num in range(1, 5):
        ev = Events.Event('data', str(num), "event:"+str(num))
        service.eventQueue.put(ev)
        time.sleep(1)

    service.stop()
