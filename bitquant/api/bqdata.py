import logging
import time
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import pymysql.cursors

params = {
    'db_host': '10.1.3.96',
    'db_port': 3306,
    'db_user': 'bitquant_test',
    'db_password': 'bitquant_test',
    'db_name': 'bitquant_test',
}

def get_kline(market, symbol, period, start_date, end_date):
    
    engine = create_engine('mysql+pymysql://%s:%s@%s:%d/%s' % (params['db_user'], params['db_password'], params['db_host'], params['db_port'], params['db_name']))
    
    start_time = time.mktime(time.strptime(start_date, "%Y%m%d"))
    end_time = time.mktime(time.strptime(end_date, "%Y%m%d"))

    querySQL = "select kid,count,amount,vol,open,close,high,low,create_date from kline where market='%s' and symbol='%s' and period='%s' and kid>='%d' and kid<='%d' order by kid asc" % (
        market, symbol, period, start_time, end_time)
    try:
        df = pd.read_sql_query(querySQL, engine)
    except BaseException as e:
        logging.error(e)
        df = None
    
    return df
    

def get_kline2(market, symbol, period, start_date, end_date):
    db = pymysql.connect(host='10.1.3.96', port=3306, user='bitquant_test', password='bitquant_test', db='bitquant_test',
                         charset='utf8', cursorclass=pymysql.cursors.DictCursor)

    # 通过cursor创建游标
    cursor = db.cursor()
    data = None

    start_time = time.mktime(time.strptime(start_date, "%Y%m%d"))
    end_time = time.mktime(time.strptime(end_date, "%Y%m%d"))

    try:
        querySQL = "select kid,count,amount,vol,open,close,high,low,create_date from kline where market='%s' and symbol='%s' and period='%s' and create_date>='%d' and create_date<='%d' order by kid asc" % (
            market, symbol, period, start_time, end_time)
        cursor.execute(querySQL)
        data = cursor.fetchall()
        
    except BaseException as e:
        logging.error(e)

    db.close()
    return data



if __name__ == '__main__':
    
    data = get_kline('huobi', 'ethusdt', '1day', '20180101', '20180818')
    print(data)
