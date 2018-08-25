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
from bitquant.strategy import strategy_context as sctx

class StrategyWorker(worker.Worker):
    def run(self):
        task_data = self.task.data
        module_name = 'bitquant.users_strategy.'+task_data['id']
        module_strategy = importlib.import_module(module_name)
        if module_strategy == None:
            logging.error('import module ['+module_name+'] error')
            return

        self.freq = task_data['type']
        self.strategy = task_data['id']

        func_name = 'handle_data'
        if task_data['type'] == 'tick':
            func_name = 'handle_tick'

        handle_func = getattr(module_strategy, func_name)
        if handle_func == None:
            logging.error('import module ['+module_name+'] fun['+func_name+']')
            return

        logging.debug('excute ['+module_name+'] fun['+func_name+']')

        strategy_context = sctx.StrategyContext(
            task_data['type'], task_data['id'], task_data['market'], task_data['uid'], task_data['did'])

        handle_func(strategy_context)


class StrategyTickWorker(worker.Worker):
    def run(self):
         # 连接MySQL数据库
        db = mysql_db.Mysql()
        cursor = db._cursor

        topic = self.task.data['dtype']
        if self.task.data['dtype'] == 'kline':
            topic = topic + '.' + \
                self.task.data['symbol'] + '.' + self.task.data['period']

        sql_query = "SELECT * FROM strategy_tick  WHERE market='%s' and topic='%s' and status='00'" % (
            self.task.data['market'], topic)
        try:
            results = cursor.execute(sql_query)
        except BaseException as ex:
            logging.error(ex)
            db.dispose(0)
            return

        results = cursor.fetchall()
        for row in results:
            action = row['action']
            logging.debug(action+":"+row['data'])

            task_data = json.loads(row['data'])
            task_data['id'] = row['strategy_id']
            task_data['uid'] = row['uid']
            task_data['type'] = 'tick'
            task_data['market'] = self.task.data['market']
            task_data['did'] = self.task.data['did']

            ctx = context.get_context()
            if ctx != None:
                ctx['app'].pub_task(None, action, '0', task_data)

            sql_update = "update strategy_tick set last_run_time=%d where id='%s'" % (
                time.time(), row['id'])
            try:
                cursor.execute(sql_update)
                db.commit()
            except BaseException as ex:
                logging.error(ex)
                db.rollback()
                break

        db.dispose()
