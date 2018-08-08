import threading
import time 
import logging
from bitquant.core import Service

'''
Market data API
'''

class EXBrokerService(Service.Service):
    def __init__(self):
        Service.Service.__init__(self, "EXBroker", TaskProccess)
        self.taskHandler = TaskProccess
        
def TaskProccess(task):
    logging.debug(task.data)
    
if __name__ == "__main__":
    service = EXBrokerService()
    service.start()

    for num in range(1, 5):
        task = Service.Task('data', str(num), "task:"+str(num))
        service.workQuque.put(task)
        time.sleep(1)

    service.stop()
