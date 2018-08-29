# -*- coding: utf-8 -*-

# !/usr/bin/env python3


from core.coreFramework.coreEvents.userEventHandler import UserEventHandler
from core.coreFramework.coreEvents.userEventHandler import UserEventType,UserEvent

import datetime
import sys


class LogEvent(UserEvent):

    def __init__(self, event_handler, log_dir, log_level, log_msg):
        self.datetime = datetime.datetime.now()
        self.log_dir = log_dir
        self.log_level = log_level
        self.log_msg = log_msg
        super().__init__(event_handler, UserEventType.LOG)

    def __str__(self):
        return '%s : [%s] %s\r\n' % (self.datetime, self.log_level, self.log_msg)


class DataEvent(UserEvent):

    def __init__(self, event_handler, data_dir, data):
        self.time = datetime.datetime.now()
        self.data_dir = data_dir
        self.data = data
        super().__init__(event_handler, UserEventType.DATA)

    def __str__(self):
        return '%s,%s\r\n' % (self.time, self.data)


if __name__ == '__main__':
    log_event = LogEvent(None, None, 'testlog', 'debug')
    print(log_event)


class Log2FileEventHandler(UserEventHandler):

    def __init__(self):
        super().__init__()

    def on_user_event(self, event):

        if event.event_type == UserEventType.LOG:
            # save log to file
            try:
                with open('%s.log' %(datetime.datetime.now().strftime('%Y%m%d')), 'a', encoding='utf8') as f:
                    f.write('%s\r\n' %(event))
            except:
                print(sys.exc_info())

        elif event.event_type == UserEventType.DATA:
            # save data to file
            try:
                with open('%s.csv' % (datetime.datetime.now().strftime('%Y%m%d')), 'a', encoding='utf8') as f:
                    f.write('%s\r\n' % (event))
            except:
                print(sys.exc_info())
        pass


class Log2ViewEventHandler(UserEventHandler):

    def __init__(self):
        super().__init__()

    def on_user_event(self, event):

        if event.event_type == UserEventType.LOG:
            # save log to file
            pass

        elif event.event_type == UserEventType.DATA:
            # save data to file
            pass
        pass


if __name__ == '__main__':
    logHandler = Log2FileEventHandler()

    logHandler.handle_event(LogEvent(None, 's1-t1', 'debug', 'testlog'))