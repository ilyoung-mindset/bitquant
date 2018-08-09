import logging

from bitquant.core import Task
from bitquant.core import Worker


class MarketInnerWorker(Worker.Worker):
    def run(self):
        print("market inner worker:"+self.task.action+" data:"+self.task.data)


class Router(Worker.Router):
    def newWorker(self, task):
        return MarketInnerWorker(task)

