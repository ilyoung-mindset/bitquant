import logging
import json
import pymysql.cursors
import threading
import time
from bitquant.core import Task
from bitquant.core import Worker

class EXTradeWorker(Worker.Worker):
    def run(self):
        data = self.task.data
        
        #获取threading对象的标识ident
        #print(threading.currentThread)
        #print (threading.currentThread().ident)

        # 连接MySQL数据库
        db = pymysql.connect(host='10.1.3.96', port=3306, user='bitquant_test', password='bitquant_test', db='bitquant_test',
                            charset='utf8', cursorclass=pymysql.cursors.DictCursor)

        # 通过cursor创建游标
        cursor = db.cursor()

        actions = self.task.action.split('/')
        market = actions[1]

        chs = self.task.data['ch'].split('.')
        symbol = chs[1]
        records = data['tick']['data']

        for record in records :
            date = time.strftime("%Y%m%d", time.localtime())
            datetime = time.strftime("%Y%m%d%H%M%S", time.localtime())
            sql = "INSERT INTO `trade` (`market`, `symbol`, `price`,`amount`,`time`,`direction`,`trade_id`,`create_date`,`create_time`) VALUES ('%s', '%s', '%G', '%G', '%d', '%s', '%d','%s','%s')" % (
                market, symbol, record['price'], record['amount'], record['ts'], record['direction'], record['id'], date, datetime)

            try:
                cursor.execute(sql)
                db.commit()
            except BaseException as e:
                logging.error(record)
                logging.error(e)
                db.rollback()

        db.close()


class Router(Worker.Router):
    def newWorker(self, task):
        return EXTradeWorker(task)
