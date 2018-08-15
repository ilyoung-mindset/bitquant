import logging
import json
import pymysql.cursors

from bitquant.core import Task
from bitquant.core import Worker


class EXMarketWorker(Worker.Worker):
    def run(self):
        pass


class Router(Worker.Router):
    def newWorker(self, task):
        return EXMarketWorker(task)
