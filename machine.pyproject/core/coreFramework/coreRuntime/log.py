# -*- coding: utf-8 -*-

# !/usr/bin/env python3


from core.coreFramework.coreEvents.eventServer import EventServer
from core.coreFramework.stationTask import StationTask

from core.coreFramework.coreRuntime.logEventHandler import LogEvent, DataEvent, Log2FileEventHandler, Log2ViewEventHandler


class Log(StationTask):

    def __init__(self):
        self.event_server = EventServer('log')
        self.event_handlers = {'log2file': Log2FileEventHandler(), 'log2view': Log2ViewEventHandler}
        super().__init__(-2,'log',None)

    def _running(self):
        while self.is_running is True or not self.event_server.empty():
            self.event_server.dispatch()

    def on_start(self, event):
        pass

    def on_pause(self, event):
        pass

    def on_stop(self, event):
        pass

    def on_reset(self, event):
        pass

    def post_log(self, event):
        for handler in self.event_handlers:
            self.event_server.post(LogEvent(handler, event.log_dir, event.log_msg, event.log_level))

    def post_data(self, event):
        for handler in self.event_handlers:
            self.event_server.post(DataEvent(handler, event.data_dir, event.data))
