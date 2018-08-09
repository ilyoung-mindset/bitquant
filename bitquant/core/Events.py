import threading
import time
import queue
import logging

'''
project events bus
'''


class Event:
     def __init__(self, e, id, data):
         self.event = e
         self.id = id
         self.data = data
