import logging
import json
from bitquant.db import mysql_db
import threading
import time
from bitquant.core import worker


class EXTradeWorker(worker.Worker):
    def run(self):
        data = self.task.data
        
        db = mysql_db.Mysql()
        cursor = db._cursor

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

        db.dispose()
