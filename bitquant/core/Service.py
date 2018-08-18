import threading
import time
import queue
import logging

from bitquant.core import Events

'''
project Service base class
'''

class ServiceThread(threading.Thread):
    def __init__(self, service, name, q, handler):
        threading.Thread.__init__(self)
        # 初始化
        # self.threadID = threadID
        self.name = name
        self.eventQueue = q
        self.eventHandler = handler
        self.service = service

    def run(self):
        logging.debug("service run ...")
        while True:
            ev = self.eventQueue.get()

            if ev.event == 'quit':
                logging.info('service['+self.name+'] quit')
                break
            
            self.eventHandler(ev, service=self.service)
            

class Service:
    def __init__(self, ctx, name, proccess, params=None):
        self.ctx = ctx
        self.eventQueue = queue.Queue()
        self.name = name
        self.thread = ServiceThread(self, self.name, self.eventQueue, proccess)
        self.params = params
        
    def before_start(self):
        pass

    def after_start(self):
        pass

    def start(self):
        logging.debug("service["+self.name+"] start ...")
        self.thread.start()

    def before_stop(self):
        pass

    def stop(self):
        self.before_stop()
        logging.debug("service["+self.name+"] stop ...")
        
        ev = Events.Event('quit', str(1), "quit request")
        self.eventQueue.put(ev)
    
    


class ServiceMgr:
    def __init__(self, ctx, services):
        self.ctx = ctx
        self.services = services
    
    def start(self):
        for k in self.services.keys():
            service = self.services[k]
            service.before_start()
            service.start()
            service.before_stop()


    def stop(self):
        for k in self.services.keys():
            service = self.services[k]
            service.before_stop()
            service.stop()

def EventProccess(e):
    print(e.data)

if __name__ == "__main__":
    services = {
        'test': Service(None, "test", EventProccess)
    }
    mgr = ServiceMgr(None, services)

    mgr.start()

    for num in range(1, 20):
        ev = Events.Event('data', str(num), "event:"+str(num))
        services['test'].eventQueue.put(ev)
        time.sleep(1)

    mgr.stop()
