# -*- coding: utf-8 -*-
import threading
import time
import logging
import websocket
import gzip
import time
import queue
import json

from bitquant.core import service
from bitquant.core import events
from bitquant.ex_broker.huobi import huobi_rest

'''
Hadax Market websocket API
'''

class WSThread(threading.Thread):
    def __init__(self, q, service):
        threading.Thread.__init__(self)
        self.service = service
        self.lastMsgID = {}
        # 初始化
        self.eventQueue = q

    def run(self):
        while True:
            self.connect()
            self.sub_topics()
            r = self.process()
            self.ws.close()
            
            if r:
                return;

           

    def process(self):
        
        while(1):
            try:
                compressData = self.ws.recv()
                result = gzip.decompress(compressData).decode('utf-8')
            except BaseException as e:
                logging.error(e)
                return False
            
           
            if result[:7] == '{"ping"':
                ts = result[8:21]
                pong = '{"pong":'+ts+'}'
                self.ws.send(pong)
                self.sub_topics()

            else:
                if self.service.ctx == None :
                    print(result)

                else :
                   # print("raw: "+result);
                    data = json.loads(result)
                    if data.__contains__('ch'):
                        if self.lastMsgID.__contains__(data['ch']):
                            if self.lastMsgID[data['ch']] == data['ts']:
                                continue
                        
                        self.lastMsgID[data['ch']] = data['ts']

                        chs = data['ch'].split('.')
                        ch = chs[2]
                        self.service.ctx['app'].pub_task(
                            None, 'exbroker/hadax/ws/'+ch, '0', data)
                    else:
                        logging.debug("data:"+result)
            
            r = self.event_process()
            if r :
                logging.info('worker thread quit')
                return True

    def connect(self):
        logging.debug("worker run ...")
        while(1):
            proxy_host = None
            if self.service.params['http_proxy_host'] != None:
                proxy_host = self.service.params['http_proxy_host']
                proxy_port = self.service.params['http_proxy_port']

            hadax_url = self.service.params['websocket']['url']
            self.ws = websocket.WebSocket()

            try:
                if proxy_host == None:
                    logging.debug("start connect :"+hadax_url)
                    self.ws.connect(hadax_url)
                else:
                    logging.debug("start connect:["+hadax_url +
                                  "] proxy:[" + proxy_host+":"+str(proxy_port)+"]")
                    self.ws.connect(
                        hadax_url, http_proxy_host=proxy_host, http_proxy_port=proxy_port)
                break
            except:
                logging.error('connect ws error,retry...')
                time.sleep(5)

    def sub_topics(self):
        for reqData in self.service.params['websocket']['subs']:
            json_str = json.dumps(reqData)
            logging.debug("sub :"+json_str)
            self.ws.send(json_str)
                
    def event_process (self):
        while self.eventQueue.qsize() > 0:
            event = self.eventQueue.get()
            if event.event == 'quit':
                return True
            
            if event.event == 'req':
                json_str = json.dumps(event.data)
                logging.debug("req :"+json_str)
                self.ws.send(json_str)

class HadaxService(service.Service):
    def __init__(self, ctx, params=None):
        service.Service.__init__(self, ctx, "HadaxService", params)
        self.WSQueue = queue.Queue()
        self.WSThread = WSThread(self.WSQueue, self)

    def start(self):
        service.Service.start(self)
        self.WSThread.start()
        self.ctx['app'].evt_mng.sub_event('market.hadax.get', self)

    def stop(self):
        ev = events.Event('quit', str(1), "quit request")
        self.WSQueue.put(ev)
        service.Service.stop(self)
    
    def event_process(self, e, service=None):
        if e.event == 'market.hadax.get':
            if e.data['topic'] == 'kline':
                huobi = huobi_rest.HuobiREST(
                    market_url="https://api.hadax.com", trade_url="https://api.hadax.com", params=service.params)
                data = huobi.get_kline(
                    e.data['symbol'], e.data['period'], e.data['size'])
                service.ctx['app'].pub_task(
                    None, 'exbroker/hadax/rest/kline', '0', data)

if __name__ == "__main__":
    service = HadaxService(None)
    service.start()

