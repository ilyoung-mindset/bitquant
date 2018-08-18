import logging
import pymysql.cursors
import time

params = {
    'db_host': '10.1.3.96',
    'db_port': 3306,
    'db_user': 'bitquant_test',
    'db_password': 'bitquant_test',
    'db_name': 'bitquant_test',
}

def get_kline(market, symbol, period, start_date, end_date):
    db = pymysql.connect(host='10.1.3.96', port=3306, user='bitquant_test', password='bitquant_test', db='bitquant_test',
                         charset='utf8', cursorclass=pymysql.cursors.DictCursor)

    # 通过cursor创建游标
    cursor = db.cursor()
    data = None

    try:
        querySQL = "select * from kline where market='%s' and symbol='%s' and period='%s' and create_date>='%s' and create_date<='%s'" % (
        market, symbol, period, start_date, end_date)
        cursor.execute(querySQL)
        data = cursor.fetchall()
        
    except BaseException as e:
        logging.error(e)

    db.close()
    return data



if __name__ == '__main__':
    params = {}

    data = get_kline('huobi', 'ethusdt', '1day', '20180101', '20180818')
    print(data)
