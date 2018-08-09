import threading
import time
import queue
import logging

'''
project task proccess
'''

class Task:
    def __init__(self, ctx, action, id, data):
        self.ctx = ctx

        self.action = action
        self.id = id
        self.data = data
