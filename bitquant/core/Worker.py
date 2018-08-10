import threading
import time
import queue
import logging
from bitquant.core import Service
from bitquant.core import Events
from bitquant.core import Task

'''
Market data API
'''

class Worker:
    def __init__(self, task):
        self.task = task

    def run(self):
        print("test worker:"+self.task.action)

class Router:
    def newWorker(self, task):
        return Worker(task)

class WorkerThread(threading.Thread):
    def __init__(self, q, ws):
        threading.Thread.__init__(self)
        self.ws = ws

        # 初始化
        self.TaskQueue = q

    def run(self):
        logging.debug("worker run ...")
        while True:
            task = self.TaskQueue.get()

            if task.action == 'quit':
                logging.info('worker thread quit')
                break
            
            if self.ws.routes.__contains__(task.action):
                worker = self.ws.routes[task.action].newWorker(task)
                if worker == None:
                    logging.error("create worker error")
                    continue

                worker.run()
            else: 
                logging.warning("task["+task.action+"] not found.")

class WorkerService(Service.Service):
    def __init__(self, ctx, routes):
        Service.Service.__init__(self, ctx, "Worker", EventProccess)
        self.eventHandler = EventProccess
        self.taskQueue = queue.Queue()
        self.workThread = WorkerThread(self.taskQueue, self)
        self.routes = routes

    def start(self):
        Service.Service.start(self)
        self.workThread.start()
    
    def stop(self):
        quitTask = Task.Task(self, 'quit', str(0), "quit task thread")
        self.taskQueue.put(quitTask)

        Service.Service.stop(self)
    
    def pubTask(self, ctx, action, id, data):
        task = Task.Task(ctx, action, id, data)
        self.taskQueue.put(task)


def EventProccess(e):
    logging.debug(e.data)


if __name__ == "__main__":
    routes = {'test':Router()}
    service = WorkerService(None, routes)
    service.start()

    for num in range(1, 5):
        task = Task.Task(service, 'test', str(num), "test task:"+str(num))
        service.taskQueue.put(task)
        time.sleep(1)

    service.stop()


