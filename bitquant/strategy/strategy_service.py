import threading
import time
import queue
import logging
import json
from bitquant.db import mysql_db
from bitquant.core import service
from bitquant.core import events
from bitquant.core import worker
import importlib
from bitquant.core import context

'''
Strategy service
'''

class WorkThread(threading.Thread):
    def __init__(self, q, service):
        threading.Thread.__init__(self)
        self.service = service
        # 初始化
        self.taskQueue = q

    def run(self):
        # 连接MySQL数据库
        db = mysql_db.Mysql()
        cursor = db._cursor

        last_sec = None

        while True:
            r = self.task_process()
            if r:
                break

            cur_time = time.localtime()
            cur_sec = time.strftime("%Y%m%d%H%M", cur_time)
            cur_min = time.strftime("%Y%m%d%H%M", cur_time)
            cur_day = time.strftime("%Y%m%d", cur_time)

            if last_sec != None and last_sec == cur_sec:
                time.sleep(1)
                continue

            sql_query = "SELECT * FROM strategy_schedule  WHERE next_run_time < '%d' and status='00'" % time.time()
            try:
                results = cursor.execute(sql_query)
            except BaseException as ex:
                logging.error(ex)
                break

            results = cursor.fetchall()
            for row in results:
                action = row['action']

                last_time = time.localtime(row['last_run_time'])

                if row['freq'] == 'd' and cur_time.tm_mon == last_time.tm_mon and cur_time.tm_mday == last_time.tm_mday:
                    continue

                logging.debug(action+":"+row['data'])

                did = time.mktime(time.strptime(cur_sec, '%Y%m%d%H%M'))
                if row['freq'] == 'd':
                    did = time.mktime(time.strptime(cur_day, '%Y%m%d'))

                task_data = json.loads(row['data'])
                task_data['id'] = row['strategy_id']
                task_data['uid'] = row['uid']
               
                task_data['did'] = did

                next_time1 = time.strftime( "%Y%m%d%H%M", time.localtime(time.time()+60))
                next_time = time.mktime( time.strptime(next_time1, '%Y%m%d%H%M'))
                if row['freq'] == 'd':
                    next_time1 = time.strftime( "%Y%m%d", time.localtime(time.time()+60*60*24))
                    next_time = time.mktime( time.strptime(next_time1, '%Y%m%d'))
                

                if self.service.ctx != None:
                    self.service.ctx['app'].pub_task( None, action, '0', task_data)

                sql_update = "update strategy_schedule set last_run_time=%d, next_run_time=%d where id='%s'" % (
                    time.time(), next_time, row['id'])
                try:
                    cursor.execute(sql_update)
                    db.commit()
                except BaseException as ex:
                    logging.error(ex)
                    db.rollback()
                    break

            last_sec = cur_sec

        db.dispose()


    def task_process(self):
        while self.taskQueue.qsize() > 0:
            worker = self.taskQueue.get()
            if worker.task.action == 'quit':
                return True

class StrategyService(service.Service):
    def __init__(self, ctx):
        service.Service.__init__(self, ctx, "StrategyService")
        self.taskQueue = queue.Queue()
        self.workThread = WorkThread(self.taskQueue, self)

    def start(self):
        service.Service.start(self)
        self.workThread.start()

    def stop(self):
        quitTask = worker.Task(self, 'quit', str(0), "quit task thread")
        wk = worker.Worker(quitTask)

        self.taskQueue.put(wk)
        service.Service.stop(self)


if __name__ == "__main__":
    svr = StrategyService(None)
    svr.start()

    for num in range(1, 5):
        time.sleep(1)

    svr.stop()
