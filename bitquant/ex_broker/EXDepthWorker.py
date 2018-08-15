import logging
import json
import pymysql.cursors
import time
from bitquant.core import Task
from bitquant.core import Worker


class EXDepthWorker(Worker.Worker):
    def run(self):
        data = self.task.data
       
        return
        # 连接MySQL数据库
        db = pymysql.connect(host='10.1.3.96', port=3306, user='bitquant_test', password='bitquant_test', db='bitquant_test',
                             charset='utf8', cursorclass=pymysql.cursors.DictCursor)

        # 通过cursor创建游标
        cursor = db.cursor()

        actions = self.task.action.split('/')
        market = actions[1]

        chs = self.task.data['ch'].split('.')
        symbol = chs[1]
        record = data['tick']
        ktype = chs[3]

        date = time.strftime("%Y%m%d", time.localtime())
        datetime = time.strftime("%Y%m%d%H%M%S", time.localtime())

        sql = "INSERT INTO `depth` (`market`, `symbol`,`ktype`, `kid`,`count`,`amount`,`open`,`close`,`low`,`high`,`vol`,`create_date`,`create_time`) VALUES ('%s', '%s', '%s', '%d', '%d', '%G', '%G', '%G','%G','%G','%G','%s','%s')" % (
            market, symbol, ktype, record['id'], record['count'], record['amount'], record['open'], record['close'], record['low'], record['high'], record['vol'], date, datetime)
        try:

            querySQL = "SELECT count(1) as num from kline where market='%s' and symbol='%s' and ktype='%s' and kid='%d'" % (
                market, symbol, ktype, record['id'])
            cursor.execute(querySQL)
            row = cursor.fetchone()
            if row != None and row['num'] > 0:
                return

        except BaseException as e:
            logging.error(data)
            logging.error(e)

        try:

            cursor.execute(sql)
            db.commit()
        except BaseException as e:
            logging.error(data)
            logging.error(e)
            db.rollback()

        finally:
            db.close()


class Router(Worker.Router):
    def newWorker(self, task):
        return EXDepthWorker(task)
