import threading
import time
import queue
import logging
from bitquant.core import service
from bitquant.core import worker

'''
Stratery service
'''


class EXDepthWorker(worker.Worker):
    def run(self):
        pass

class WorkThread(threading.Thread):
    def __init__(self,  q, ws):
        threading.Thread.__init__(self)
        self.ws = ws
        # 初始化
        self.taskQueue = q

    def run(self):
        while True:
            #TODO: 处理策略执行

            r = self.task_process()
            if r:
                break

            time.sleep(1)

    def task_process(self):
        while self.taskQueue.qsize() > 0:
            worker = self.taskQueue.get()
            if worker.task.action == 'quit':
                return True

class StrateryService(service.Service):
    def __init__(self, ctx, params=None):
        service.Service.__init__(self, ctx, "Schedule", params)
        self.eventHandler = self.event_process
        self.taskQueue = queue.Queue()
        self.workThread = WorkThread(self.taskQueue, self)

    def start(self):
        service.Service.start(self)
        self.workThread.start()

    def stop(self):
        quitTask = worker.Task(self, 'quit', str(0), "quit task thread")
        w = worker.Worker(quitTask)
        self.taskQueue.put(w)

        service.Service.stop(self)


if __name__ == "__main__":

    s = StrateryService(None)
    s.start()

    for num in range(1, 5):
        time.sleep(1)

    s.stop()
