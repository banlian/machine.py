# -*- coding: utf-8 -*-


'''
created on 2018-01-16

@author: zzz
'''

from enum import Enum
import time


class UserEvent(object):

    def __init__(self, event_handler, event_type):
        self.time = time.time()
        self.event_handler = event_handler
        self.event_type = event_type

    def execute(self):
        if self.event_handler is not None:
            self.event_handler.handle_event(self)

    def __lt__(self, other):
        return self.time < other.time

    def __str__(self):
        return 'Event %s %s' %(type(self.event_handler), self.event_type)


class UserEventType(Enum):
    # get  io
    SIGNAL = 1,
    ALARM = 2,

    # user control
    START = 3,
    STOP = 4,
    RESET = 5,
    PAUSE = 6,
    CONTINUE = 7,

    # motion
    AXISSERVO = 8,
    AXISHOME = 9,
    AXISMOVE = 10,

    # set io
    SETIO = 11,
    WAITIO = 12,

    # misc
    LOG = 13,
    DATA = 14,