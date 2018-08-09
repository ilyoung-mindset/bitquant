import threading
import time 
import logging
from bitquant.core import Service
from bitquant.core import Events

'''
Market data API
'''

class EXBrokerService(Service.Service):
    def __init__(self):
        Service.Service.__init__(self, "EXBroker", EventProccess)
        self.eventHandler = EventProccess
        

def EventProccess(e):
    logging.debug(e.data)
    
if __name__ == "__main__":
    service = EXBrokerService()
    service.start()

    for num in range(1, 5):
        ev = Events.Event('data', str(num), "event:"+str(num))
        service.eventQueue.put(ev)
        time.sleep(1)

    service.stop()
