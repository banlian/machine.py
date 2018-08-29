# -*- coding: utf-8 -*-

# !/usr/bin/env python3


from core.coreFramework.coreEvents.eventServer import EventServer
from core.coreFramework.stationTask import StationTask


class Main(StationTask):

    def __init__(self, station):
        self.event_server = EventServer('main')
        super().__init__(0, 'main', station)

    def _running(self):
        while self.is_running is True or not self.event_server.empty():
            self.station.runtime.update()
            self.event_server.dispatch()

    def on_start(self, event):
        pass

    def on_pause(self, event):
        pass

    def on_stop(self, event):
        pass

    def on_reset(self, event):
        pass

    def post_event(self, event, priority):
        self.event_server.post(event, priority)
