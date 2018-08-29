# -*- coding: utf-8 -*-

# !/usr/bin/env python3


from core.coreFramework.coreRuntime.mainEventHandler import MainEventHandler
from core.coreFramework.coreRuntime.alarmEventHandler import UserEventType, SystemAlarm


class SetIO(MainEventHandler):

    def __init__(self, task):
        self.io = None
        self.io_status = None
        super().__init__(task)

    def on_event_handle(self, event):
        if event.event_type == UserEventType.SETIO:
            ret = [self.io[i].set(self.io_status[i]) for i in range(len(self.io))]
            if any(ret):
                self.task.error(SystemAlarm.DO_ERROR, ','.join([io.name for io in self.io]))
            return 0

    def on_event_handling(self):
        self.state = 'done'

    def setio(self, io, io_status):
        self.io = io
        self.io_status = io_status
        self.post_event(UserEventType.SETIO)
        return self.wait_event_done(-1)


class SetDo(SetIO):

    def setio(self, io, io_status):
        self.io = [self.task.station.runtime.do[do] for do in io]
        return super().setio(self.io, io_status)


class SetVio(SetIO):

    def setio(self, io, io_status):
        self.io = [self.task.station.runtime.vio[do] for do in io]
        return super().setio(self.io, io_status)


class WaitIO(MainEventHandler):

    def __init__(self, task):
        self.io = None
        self.io_status = None
        self.timeout = 0
        super().__init__(task)

    def on_event_handling(self):
        if all([self.io[i].check(self.io_status[i]) for i in range(len(self.io))]):
            self.state = 'done'
        elif 0 <= self.timeout < self.task.station.runtime.time_ticks - self._start_tick:
            self.state = 'timeout'

    def waitio(self, io, io_status, timeout, is_error):
        self.io = io
        self.io_status = io_status
        self.timeout = timeout
        self.post_event(UserEventType.WAITIO)
        return self.wait_event_done(timeout)


class WaitDi(WaitIO):

    def waitio(self, io, io_status, timeout, is_error):
        self.io = [self.task.station.runtime.di[i] for i in io]
        return super().waitio(self.io, io_status, timeout, is_error)


class WaitVio(WaitIO):

    def waitio(self, io, io_status, timeout, is_error):
        self.io = [self.task.station.runtime.vio[i] for i in io]
        return super().waitio(self.io, io_status, timeout, is_error)


if __name__ == '__main__':
    pass
