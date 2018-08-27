import threading
from flask import Flask
from flask import request
import json

api_gateway = Flask(__name__)

def test():
    print(request)

@api_gateway.route('/strategy/backtest', methods=['GET', 'POST'])
def stratgy_backtest():
    if request.method == 'POST':
        data = {
            'result':'ok'
        }
    else :
        data = {
            'result': 'fail'
        }

    retdata = json.dumps(data)
    print(request)
    print('test ...')
    print(threading.currentThread().ident)

    test()
    
    return retdata


if __name__ == '__main__':
    api_gateway.run()
  
    print("api gateway startup...")
