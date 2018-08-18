import threading
import time
import queue
import logging
from bitquant.core import Service
from bitquant.core import Events
from bitquant.core import Task
from bitquant.core import Worker

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
        s = False

        while True:
            ev = Events.Event('market.huobi.get', str(
                 1), {'topic': 'kline', 'symbol': 'ethusdt', 'period': '1day', 'size': 2000})
            
            if not s:
                r = self.service.ctx['app'].evt_mng.pub_event(ev)
                if r:
                    s = True

            r = self.TaskProcess()
            if r:
                break;

            time.sleep(60)
            

    def TaskProcess (self):
        while self.taskQueue.qsize() > 0:
            worker = self.taskQueue.get()
            if worker.task.action == 'quit':
                return True
            
           

class EXBrokerService(Service.Service):
    def __init__(self, ctx):
        Service.Service.__init__(self, ctx, "EXBroker", EventProccess)
        self.eventHandler = EventProccess
        self.taskQueue = queue.Queue()
        self.workThread = WorkerThread(self.taskQueue, self)

    def start(self):
        Service.Service.start(self)
        self.workThread.start()

    def stop(self):
        quitTask = Task.Task(self, 'quit', str(0), "quit task thread")
        worker = Worker.Worker(quitTask)

        self.taskQueue.put(worker)

        Service.Service.stop(self)

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
