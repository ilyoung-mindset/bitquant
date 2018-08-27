import json
import urllib
import urllib.parse
import urllib.request
import requests
import logging

def _init(params):
    global _params
    _params = params


def back_test(market, symbol, start_date, end_date, amount):
    '''
    back test
    '''
    data = {
        'market': market,
        'symbol': symbol,
        'dtype': '1min',
        'start_date': start_date,
        'end_date': end_date,
        'amount': amount,
    }
    url_str = 'http://127.0.0.1:5000/strategy/backtest'
    result = http_post_request(url_str, data)

    print(result)
    

def http_get_request(url, params, add_to_headers=None):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }

    if add_to_headers:
        headers.update(add_to_headers)

    postdata = urllib.parse.urlencode(params)
    response = requests.get(url, postdata, headers=headers, timeout=5)

    try:

        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        print("httpGet failed, detail is:%s,%s" % (response.text, e))
        return


def http_post_request(url, params, add_to_headers=None):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json'
    }
    if add_to_headers:
        headers.update(add_to_headers)

    postdata = json.dumps(params)
    response = requests.post(url, postdata, headers=headers, timeout=10)
    try:

        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        print("httpPost failed, detail is:%s,%s" % (response.text, e))
        return
