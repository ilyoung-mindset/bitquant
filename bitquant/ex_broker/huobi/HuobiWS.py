# -*- coding: utf-8 -*-
#author: 半熟的韭菜
import threading
import time
import logging
import websocket
import gzip
import time
import queue
import json

from bitquant.core import Service
from bitquant.core import Events

'''
Huobi Market websocket API
'''

class WSThread(threading.Thread):
    def __init__(self, q, service):
        threading.Thread.__init__(self)
        self.service = service

        # 初始化
        self.eventQueue = q

    def run(self):
        while True:
            self.connect()
            self.subTopics()
            r = self.process()
            if r:
                return;
        
    def process(self):
        
        while(1):
            compressData = self.ws.recv()
            result = gzip.decompress(compressData).decode('utf-8')
            if result[:7] == '{"ping"':
                ts = result[8:21]
                pong = '{"pong":'+ts+'}'
                self.ws.send(pong)
                self.subTopics()

            else:
                if self.service.ctx == None :
                    print(result)

                else :
                    logging.debug(result)
                    self.service.ctx['app'].pubTask(None, 'exbroker/huobiws', '0', result)
            
            r = self.EventProcess()
            if r :
                logging.info('worker thread quit')
                return True

    def connect(self):
        logging.debug("worker run ...")
        while(1):
            proxy_host = self.service.ctx['params']['network']['http_proxy']['host']
            proxy_port = self.service.ctx['params']['network']['http_proxy']['port']
            huobi_url = self.service.ctx['params']['market']['huobi']['websocket']['url']
            self.ws = websocket.WebSocket()

            try:
                if proxy_host == None:
                    logging.debug("start connect :"+huobi_url)
                    self.ws.connect(huobi_url)
                else:
                    logging.debug("start connect:["+huobi_url +
                                  "] proxy:[" + proxy_host+":"+str(proxy_port)+"]")
                    self.ws.connect(
                        huobi_url, http_proxy_host=proxy_host, http_proxy_port=proxy_port)
                break
            except:
                logging.error('connect ws error,retry...')
                time.sleep(5)

    def subTopics(self):
        # 订阅 KLine 数据
        #tradeStr = """{"sub": "market.ethusdt.kline.1min","id": "id10"}"""
        #self.ws.send(tradeStr)

        #tradeStr = """{"sub": "market.btcusdt.kline.1min","id": "id10"}"""
        #ws.send(tradeStr)

        # 请求 KLine 数据
        # tradeStr="""{"req": "market.ethusdt.kline.1min","id": "id10", "from": 1513391453, "to": 1513392453}"""

        #订阅 Market Depth 数据
        # tradeStr="""{"sub": "market.ethusdt.depth.step5", "id": "id10"}"""

        #请求 Market Depth 数据
        # tradeStr="""{"req": "market.ethusdt.depth.step5", "id": "id10"}"""

        #订阅 Trade Detail 数据
        # tradeStr="""{"sub": "market.ethusdt.trade.detail", "id": "id10"}"""

        #请求 Trade Detail 数据
        # tradeStr="""{"req": "market.ethusdt.trade.detail", "id": "id10"}"""

        #请求 Market Detail 数据
        # tradeStr="""{"req": "market.ethusdt.detail", "id": "id12"}"""

        for reqData in self.service.ctx['params']['market']['huobi']['websocket']['subs']:
            json_str = json.dumps(reqData)
            logging.debug("sub :"+json_str)
            self.ws.send(json_str)
                
    def EventProcess (self):
        while self.eventQueue.qsize() > 0:
            event = self.eventQueue.get()
            if event.event == 'quit':
                return True
            
            if event.event == 'req':
                json_str = json.dumps(event.data)
                logging.debug("req :"+json_str)
                self.ws.send(json_str)

class HuobiWSService(Service.Service):
    def __init__(self, ctx):
        Service.Service.__init__(self, ctx, "HuobiWSService", EventProccess)
        self.eventHandler = EventProccess
        self.WSQueue = queue.Queue()
        self.WSThread = WSThread(self.WSQueue, self)

    def start(self):
        Service.Service.start(self)
        self.WSThread.start()

    def stop(self):
        ev = Events.Event('quit', str(1), "quit request")
        self.WSQueue.put(ev)
        Service.Service.stop(self)

def EventProccess(e):
    logging.debug(e.data)


if __name__ == "__main__":
    service = HuobiWSService(None)
    service.start()

