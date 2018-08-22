import threading
import time
import queue
import logging
from bitquant.core import service
from bitquant.core import events
from bitquant.core import worker

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
            ev = events.Event('market.huobi.get', str(
                 1), {'topic': 'kline', 'symbol': 'ethusdt', 'period': '1day', 'size': 2000})
            
            if not s:
                r = self.service.ctx['app'].evt_mng.pub_event(ev)
                if r:
                    s = True

            r = self.task_process()
            if r:
                break;

            time.sleep(60)
            
    def task_process(self):
        while self.taskQueue.qsize() > 0:
            worker = self.taskQueue.get()
            if worker.task.action == 'quit':
                return True
            
           
class EXBrokerService(service.Service):
    def __init__(self, ctx):
        service.Service.__init__(self, ctx, "EXBroker")
        self.taskQueue = queue.Queue()
        self.workThread = WorkerThread(self.taskQueue, self)

    def start(self):
        service.Service.start(self)
        self.workThread.start()

    def stop(self):
        quitTask = worker.Task(self, 'quit', str(0), "quit task thread")
        wk = worker.Worker(quitTask)

        self.taskQueue.put(wk)
        service.Service.stop(self)
  

if __name__ == "__main__":
    service = EXBrokerService(None)
    service.start()

    for num in range(1, 5):
        ev = events.Event('data', str(num), "event:"+str(num))
        service.eventQueue.put(ev)
        time.sleep(1)

    service.stop()
