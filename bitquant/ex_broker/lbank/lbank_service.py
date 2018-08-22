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

from bitquant.core import service
from bitquant.core import events

'''
Lbank Market websocket API
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
            self.sub_topics()
            r = self.process()
            if r:
                return;
        
    def process(self):
        
        while(1):
            result = self.ws.recv()
            #result = gzip.decompress(compressData).decode('utf-8')
            data = json.loads(result)
            if data.__contains__('action') and data['action'] == 'ping':
                pong = '{"action": "pong", "pong": "'+data['ping']+'"}'
                self.ws.send(pong)
                self.sub_topics()

            else:
                if self.service.ctx == None :
                    print(result)

                else :
                    #print("raw: "+result);
                    if data.__contains__('pair'):
                        self.service.ctx['app'].pub_task(
                            None, 'exbroker/lbank/ws', '0', data)
                    else:
                        logging.debug("data:"+result)
            
            r = self.event_process()
            if r :
                logging.info('worker thread quit')
                return True

    def connect(self):
        logging.debug("worker run ...")
        while(1):
            proxy_host = self.service.ctx['params']['network']['http_proxy']['host']
            proxy_port = self.service.ctx['params']['network']['http_proxy']['port']
            lbank_url = self.service.ctx['params']['market']['lbank']['websocket']['url']
            self.ws = websocket.WebSocket()

            try:
                if proxy_host == None:
                    logging.debug("start connect :"+lbank_url)
                    self.ws.connect(lbank_url)
                else:
                    logging.debug("start connect:["+lbank_url +
                                  "] proxy:[" + proxy_host+":"+str(proxy_port)+"]")
                    self.ws.connect(
                        lbank_url, http_proxy_host=proxy_host, http_proxy_port=proxy_port)
                break
            except:
                logging.error('connect ws error,retry...')
                time.sleep(5)

    def sub_topics(self):
        for reqData in self.service.ctx['params']['market']['lbank']['websocket']['subs']:
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


class LbankWSService(service.Service):
    def __init__(self, ctx, params=None):
        service.Service.__init__(self, ctx, "LbankService", params)
        self.WSQueue = queue.Queue()
        self.WSThread = WSThread(self.WSQueue, self)

    def start(self):
        service.Service.start(self)
        self.WSThread.start()

    def stop(self):
        ev = events.Event('quit', str(1), "quit request")
        self.WSQueue.put(ev)
        service.Service.stop(self)

if __name__ == "__main__":
    service = LbankWSService(None)
    service.start()

