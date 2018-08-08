import threading
import time
import queue
import logging

'''
project Service base class
'''

class Task:
     def __init__(self, action, id, data):
         self.action = action
         self.id = id
         self.data = data 

class ServiceThread(threading.Thread):
    def __init__(self, q, handler):
        threading.Thread.__init__(self)
        # 初始化
        # self.threadID = threadID
        # self.name = name
        self.workQueue = q
        self.taskHandler = handler

    def run(self):
        logging.debug("service run ...")
        while True:
            task = self.workQueue.get()

            if task.action == 'quit':
                logging.info('service quit')
                break
            
            self.taskHandler(task)
            

class Service:
    def __init__(self, name, proccess):
        self.workQuque = queue.Queue()
        self.name = name
        self.thread = ServiceThread(self.workQuque, proccess)
        

    def start(self):
        logging.debug("service["+self.name+"] start ...")
        self.thread.start()
    
    def stop(self):
        logging.debug("service["+self.name+"] stop ...")
        task = Task('quit', str(1), "quit request")
        self.workQuque.put(task)
    
def TaskProccess(task):
        print(task.data)


if __name__ == "__main__":
    service = Service("test", TaskProccess)
    service.start()

    for num in range(1, 5):
        task = Task('data', str(num), "task:"+str(num))
        service.workQuque.put(task)
        time.sleep(1)

    service.stop()
