import threading
import time
import queue
import logging
import json
import pymysql.cursors
from bitquant.core import service
from bitquant.core import events
from bitquant.core import worker
import importlib

'''
Stratery service
'''


class StrateryWorker(worker.Worker):
    def run(self):
        task_data = self.task.data
        module_name = 'bitquant.stratery.'+task_data['id']
        module_stratery = importlib.import_module(module_name)
        if module_stratery == None:
            logging.error('import module ['+module_name+'] error')
            return

        self.freq = task_data['type']
        self.stratery = task_data['id']

        module_stratery.order = self.order

        func_name = 'handle_data'
        if task_data['type'] == 'tick':
            func_name = 'handle_tick'

        handle_func = getattr(module_stratery, func_name)
        if handle_func == None: 
            logging.error('import module ['+module_name+'] fun['+func_name+']')
            return 

        logging.info('excute ['+module_name+'] fun['+func_name+']')
        handle_func(None)
    
    def order(self, amount, price):
        print('freq[%s] buy amount[%f] price[%s]' % (self.freq, amount, price))
        logging.info('freq[%s] buy amount[%f] price[%s]' %
            (self.freq, amount, price))
        

class WorkThread(threading.Thread):
    def __init__(self, q, service):
        threading.Thread.__init__(self)
        self.service = service
        # 初始化
        self.taskQueue = q

    def run(self):
        # 连接MySQL数据库
        db = pymysql.connect(host='10.1.3.96', port=3306, user='bitquant_test', password='bitquant_test', db='bitquant_test',
                             charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()

        last_sec = None

        while True:
            r = self.task_process()
            if r:
                break

            cur_time = time.localtime()
            cur_sec = time.strftime("%Y%m%d%H%M", cur_time)
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

                task_data = json.loads(row['data'])

                if self.service.ctx != None:
                    self.service.ctx['app'].pub_task( None, action, '0', task_data)

                next_time1 = time.strftime("%Y%m%d%H%M", time.localtime(time.time()+60))
                next_time = time.mktime(time.strptime(next_time1, '%Y%m%d%H%M'))
                if row['freq'] == 'd':
                    next_time1 = time.strftime("%Y%m%d", time.localtime(time.time()+60*60*24))
                    next_time = time.mktime(time.strptime(next_time1, '%Y%m%d'))

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

        db.close()


    def task_process(self):
        while self.taskQueue.qsize() > 0:
            worker = self.taskQueue.get()
            if worker.task.action == 'quit':
                return True

class StrateryService(service.Service):
    def __init__(self, ctx):
        service.Service.__init__(self, ctx, "StrateryService")
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
    svr = StrateryService(None)
    svr.start()

    for num in range(1, 5):
        time.sleep(1)

    svr.stop()
