import logging
import json
import pymysql.cursors
import time
import uuid
from bitquant.core import worker
from bitquant.core import context


class EXMarketWorker(worker.Worker):
    def run(self):
        data = self.task.data
        
        # 连接MySQL数据库
        db = pymysql.connect(host='10.1.3.96', port=3306, user='bitquant_test', password='bitquant_test', db='bitquant_test',
                             charset='utf8', cursorclass=pymysql.cursors.DictCursor)

        actions = self.task.action.split('/')
        market = actions[1]

        chs = self.task.data['ch'].split('.')
        symbol = chs[1]
        period = chs[3]

        if actions[2] == 'ws':
            record = data['tick']
            self.update_kline_data(market, symbol, period, record, db)
            ctx = context.get_context()
            if ctx != None:
                tick_task = {'market': market, 'dtype': 'kline', 'symbol': symbol, 'did': record['id'], 'period': period}
                ctx['app'].pub_task( None, 'exbroker/kline/tick', '0', tick_task)
        else:
            for record in data['data']:
                ret = self.update_kline_data(market, symbol, period, record, db)

        db.close()


    def update_kline_data(self, market, symbol, period, record, db):
        # 通过cursor创建游标
        cursor = db.cursor()
        date = time.strftime("%Y%m%d", time.localtime())
        datetime = time.strftime("%Y%m%d%H%M%S", time.localtime())

        s_uuid = ''.join(str(uuid.uuid1()).split('-'))

        sql = "INSERT INTO `kline` (`id`, `market`, `symbol`,`period`, `kid`,`count`,`amount`,`open`,`close`,`low`,`high`,`vol`,`create_date`,`create_time`) VALUES ('%s', '%s', '%s', '%s', '%d', '%d', '%G', '%G', '%G','%G','%G','%G','%s','%s')" % (
            s_uuid, market, symbol, period, record['id'], record['count'], record['amount'], record['open'], record['close'], record['low'], record['high'], record['vol'], date, datetime)
        try:
           
            querySQL = "delete from kline where market='%s' and symbol='%s' and period='%s' and kid='%d'" % (
                market, symbol, period, record['id'])
            cursor.execute(querySQL)
           
        except BaseException  as e:
            logging.error(record)
            logging.error(e)
        try:
            cursor.execute(sql)
            db.commit()
        except BaseException as e:
            logging.error(record)
            logging.error(e)
            #db.rollback()
        
        return True
