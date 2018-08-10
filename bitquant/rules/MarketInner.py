import logging
import json

from bitquant.core import Task
from bitquant.core import Worker

markets = {

}

tx_rules = [
    #{'middle': 'eth', 'main': 'usdt', 'second':'btc', 'get': 'usdt', 'market': [ 'ethusdt', 'btcusdt', 'ethbtc'], 'water_heigh': 10, 'water_low': 0.5},
    {'middle': 'pnt', 'main': 'btc', 'second':'eth', 'get': 'pnt', 'market': ['pntbtc', 'ethbtc', 'pnteth'], 'water_heigh': 1000000, 'water_low':100000},
]

class MarketInnerWorker(Worker.Worker):
    def run(self):
      
        if not self.task.data.__contains__('ch'):
            return;

        chs = self.task.data['ch'].split('.')
        ch = chs[1]
        markets[ch] = self.task.data
        
        for rule in tx_rules:
            if(not rule['market'].__contains__(ch)):
                continue
            
            if not markets.__contains__(rule['market'][0]):
                continue

            if not markets.__contains__(rule['market'][1]):
                continue

            if not markets.__contains__(rule['market'][2]):
                continue

            
            c = markets[rule['market'][0]]['tick']['bids'][0][1]
            if c < rule['water_low']:
                continue
            
            if c > rule['water_heigh']:
                c = rule['water_heigh']
                
            print(self.task.data)
            a1 = markets[rule['market'][0]]['tick']['bids'][0][0] * c
            a2 = a1/markets[rule['market'][1]]['tick']['asks'][0][0]
            a3 = a2/markets[rule['market'][2]]['tick']['asks'][0][0]
            gap = a3-c
            print("A "+rule['middle']+":"+'{:.5f}'.format(c) + "  "+rule['main']+":"+'{:.5f}'.format(a1) + "  "+rule['second']+":"+'{:.5f}'.format(
                a2)+"   "+rule['middle']+":"+'{:.5f}'.format(a3)+"  ["+rule['middle']+" gap:"+'{:.5f}'.format(gap)+"  "+'{:.3f}'.format(gap/c)+"]")
            
            c = markets[rule['market'][2]]['tick']['bids'][0][1]
            c = markets[rule['market'][0]]['tick']['bids'][0][1]
            if c < rule['water_low']:
                continue

            if c > rule['water_heigh']:
                c = rule['water_heigh']

            b1 = markets[rule['market'][2]]['tick']['bids'][0][0] * c
            b2 = markets[rule['market'][1]]['tick']['asks'][0][0] * b1
            b3 = b2/markets[rule['market'][0]]['tick']['asks'][0][0]
            gap = b3-c
            print("B "+rule['middle']+":"+'{:.5f}'.format(c) + "  "+rule['second']+":"+'{:.5f}'.format(b1) + "  "+rule['main']+":"+'{:.5f}'.format(
                b2)+"   "+rule['middle']+":"+'{:.5f}'.format(b3)+"  ["+rule['middle']+" gap:"+'{:.5f}'.format(gap)+"  "+'{:.3f}'.format(gap/c)+"]")
            

class Router(Worker.Router):
    def newWorker(self, task):
        return MarketInnerWorker(task)

