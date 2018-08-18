import threading
import time
import queue
import logging

'''
project events bus
'''


class Event:
    def __init__(self, e, id, data, sender=None):
        self.event = e
        self.id = id
        self.sender = sender
        self.data = data


class EventMananger:
    def __init__(self):
        self.events = {}

    def sub_event(self, event_id, service):
        self.events[event_id] = service

    def unsub_event(self, event_id):
        del self.events[event_id]
    
    def pub_event(self, ev):
        if self.events.__contains__(ev.event):
            self.events[ev.event].eventQueue.put(ev)
