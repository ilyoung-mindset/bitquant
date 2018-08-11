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


class Work:
    def __init__(self, worker, task):
        self.worker = worker
        self.task = task

class Router:
    def __init__(self, options={}):
        self.options = options

    def newWorker(self, task):
        return Worker(task)
    
class WorkerThread(threading.Thread):
    def __init__(self, threadID, q, ws):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.ws = ws
        self.fifoNum = 0

        # 初始化
        self.taskQueue = q

    def run(self):
        logging.debug("["+self.threadID+"] run ...")
        while True:
            worker = self.taskQueue.get()

            if worker.task.action == 'quit':
                logging.info("["+self.threadID+' quit')
                break
            
            logging.debug("["+self.threadID+' start run task:'+worker.task.action)
            worker.run()
            
            

class WorkerService(Service.Service):
    def __init__(self, ctx, routes):
        Service.Service.__init__(self, ctx, "Worker", EventProccess)
        self.eventHandler = EventProccess
        self.taskQueue = queue.Queue()
        self.routesQueue = {}
        self.workFifoThreads = []
        self.workThreads = []
        self.fifoWorkPerThread = 3

        if self.ctx['params']['app']['worker'].__contains__('fifo_work_per_thread'):
            self.fifoWorkPerThread = self.ctx['params']['app']['worker']['fifo_work_per_thread']
            if self.fifoWorkPerThread < 1:
                self.fifoWorkPerThread = 3

        self.threadMin = 10
        if self.ctx['params']['app']['worker'].__contains__('thread_min'):
            self.threadMin = self.ctx['params']['app']['worker']['thread_min']

        for i in range(self.threadMin):
            self.workThreads.append(WorkerThread("WorkThread-"+str(i), self.taskQueue, self))

        self.routes = routes

        for k in routes.keys():
            route = routes[k]
            if not (route.options.__contains__('fifo') and route.options['fifo']):
                self.routesQueue[k] = self.taskQueue
                continue

            if len(self.workFifoThreads) > 0:
                thread = self.workFifoThreads[len(self.workFifoThreads)-1]
                if thread.fifoNum < self.fifoWorkPerThread:
                    self.routesQueue[k] = thread.taskQueue
                    thread.fifoNum += 1
                    continue

            thread = WorkerThread("WorkThread-"+str(len(self.workThreads)), queue.Queue(), self)
            self.workThreads.append(thread)
            self.workFifoThreads.append(thread)

            self.routesQueue[k] = thread.taskQueue
            thread.fifoNum += 1
        

    def start(self):
        Service.Service.start(self)
        for t in self.workThreads:
            t.start()
    
    def stop(self):
        quitTask = Task.Task(self, 'quit', str(0), "quit task thread")
        worker = Worker(quitTask)
        for t in self.workThreads:
            t.taskQueue.put(worker)

        Service.Service.stop(self)
    
    def pubTask(self, ctx, action, id, data):
        task = Task.Task(ctx, action, id, data)
        if not self.routes.__contains__(task.action):
            logging.warning("task["+task.action+"] not found.")
            return False

        worker = self.routes[task.action].newWorker(task)
        if worker == None:
            logging.error("create worker error")
            return False
        
        self.routesQueue[action].put(worker)


def EventProccess(e):
    logging.debug(e.data)


if __name__ == "__main__":
    routes = {'test', Router({'fifo': True})}
    service = WorkerService(None, routes)
    service.start()

    for num in range(1, 5):
        service.pubTask(service, 'test', str(num), "test task:"+str(num))
        time.sleep(1)

    service.stop()


