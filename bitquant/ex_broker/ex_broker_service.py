import threading
import time
import queue
import logging
import json
import pymysql.cursors
from bitquant.core import service
from bitquant.core import events
from bitquant.core import worker

'''
Market data API
'''

class WorkerThread(threading.Thread):
    def __init__(self, q, service):
        threading.Thread.__init__(self)
        self.service = service
        # 初始化
        self.taskQueue = q

    def run(self):
        first = True
        

        # 连接MySQL数据库
        db = pymysql.connect(host='10.1.3.96', port=3306, user='bitquant_test', password='bitquant_test', db='bitquant_test',
                             charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        while True:
            sql_query = "SELECT * FROM market_schedule  WHERE next_run_time < '%d'" % time.time()
            try:
                results = cursor.execute(sql_query)
            except BaseException as ex:
                logging.error(ex)
                break

            results = cursor.fetchall()
            for row in results:
                reqs = row['reqs'].split(',')
                for req in reqs:
                    req_str = row['req_tpl'] % req
                    
                    if first and row['req_first_tpl'] != None:
                        
                        req_str = row['req_first_tpl'] % req
                        
                    req_data = json.loads(req_str)
                    ev = events.Event(row['action'], str(1), req_data)
                    
                    logging.debug(row['action']+':'+req_str)
                    if self.service.ctx != None:  
                        r = self.service.ctx['app'].evt_mng.pub_event(ev)

                next_time = time.time()+60
                if row['freq'] == 'd':
                    next_time = time.time()+60*60*24
                
                sql_update = "update market_schedule set last_run_time=%d, next_run_time=%d where id='%s'" % (
                    time.time(), next_time, row['id'])
                try:
                    cursor.execute(sql_update)
                    db.commit()
                except BaseException as ex:
                    logging.error(ex)
                    db.rollback()
                    break
                
            if first:
                first = False
                
            r = self.task_process()
            if r:
                break;

            time.sleep(1)

        db.close()


    def task_process(self):
        while self.taskQueue.qsize() > 0:
            worker = self.taskQueue.get()
            if worker.task.action == 'quit':
                return True
            
           
class EXBrokerService(service.Service):
    def __init__(self, ctx):
        service.Service.__init__(self, ctx, "EXBroker")
        self.taskQueue = queue.Queue()
        self.workThread = WorkerThread(self.taskQueue, self)

    def start(self):
        service.Service.start(self)
        self.workThread.start()

    def stop(self):
        quitTask = worker.Task(self, 'quit', str(0), "quit task thread")
        wk = worker.Worker(quitTask)

        self.taskQueue.put(wk)
        service.Service.stop(self)
  

if __name__ == "__main__":
    svr = EXBrokerService(None)
    svr.start()

    for num in range(1, 5):
        time.sleep(1)

    svr.stop()
