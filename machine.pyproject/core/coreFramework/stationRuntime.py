from core.coreFramework.station import Station

from core.coreFramework.coreEvents.userEvent import UserEvent
from core.coreFramework.coreEvents.userEvent import UserEventType
from core.coreFramework.coreRuntime.main import Main
from core.coreFramework.coreRuntime.alarm import Alarm
from core.coreFramework.coreRuntime.alarm import AlarmEvent
from core.coreFramework.coreRuntime.log import *


class Runtime(object):
    RUNTIME_LOG_LEVEL = 'trace'



class StationRuntime(Station):

    def __init__(self, setid=0, name='runtime'):
        super().__init__(setid, name, self)

        self.main = Main(self)
        self.alarm = Alarm()
        self.log = Log()

        self.driver = {}
        self.stations = {0: self}
        self.tasks = {0: self.main, -1: self.alarm, -2: self.log}

        self.time_ticks = 0

    def initialize(self):
        ret = [t.start() for t in self.tasks.values() if t.setid <= 0]
        if any(ret):
            self.post_alarm(self, 'error', -9999, 'runtime initialize error')

    def terminate(self):
        if self.state == 'auto' and self.auto_state == 'running' or 'resetting':
            [s.stop() for s in self.stations.values() if s.setid > 0]

        ret = [t.stop() for t in self.tasks.values() if t.setid <= 0]
        if any(ret):
            self.post_alarm(self, 'error', -9999, 'runtime terminate error')

    def on_signal(self, event):
        self.time_ticks += 1
        super().on_signal(event)

    def update(self):
        for drv in self.driver.values():
            drv.update()
        for di in self.di.values():
            di.update()
        for do in self.do.values():
            do.update()
        for vio in self.vio.values():
            vio.update()
        for a in self.axis.values():
            a.update()
        self.post_event(self, UserEventType.SIGNAL)

    def __str__(self):
        drv = '\r\n'.join([str(o) for o in self.driver.values()])
        drv += '\r\n'
        drv += '\r\n'.join([str(o) for o in self.di.values()])
        drv += '\r\n'
        drv += '\r\n'.join([str(o) for o in self.do.values()])
        drv += '\r\n'
        drv += '\r\n'.join([str(o) for o in self.vio.values()])
        drv += '\r\n'
        drv += '\r\n'.join([str(o) for o in self.axis.values()])
        drv += '\r\n'
        drv += '\r\n'.join([str(o) for o in self.stations.values() if type(o) == Station])
        drv += '\r\n'
        drv += '\r\n'.join([str(o) for o in self.tasks.values()])
        drv += '\r\n'
        return drv

    def __repr__(self):
        return self.__str__()

    # --------------------------------------- station events methods

    def post_event(self, event_handler, event_type):
        if event_type == UserEventType.SIGNAL:
            priority = 0
        elif event_type == UserEventType.ALARM \
                or event_type == UserEventType.START \
                or event_type == UserEventType.STOP \
                or event_type == UserEventType.RESET \
                or event_type == UserEventType.PAUSE \
                or event_type == UserEventType.CONTINUE:
            priority = 1
        else:
            priority = 2
        self.main.post_event(UserEvent(event_handler, event_type), priority)

    def post_alarm(self, station, alarm_level, alarm_id, alarm_msg):
        if alarm_level == 'warning':
            self.post_event(station, UserEventType.PAUSE)
        elif alarm_level == 'error':
            self.post_event(station, UserEventType.STOP)
        self.alarm.post_event(AlarmEvent(None, station, alarm_level, alarm_id, alarm_msg))
        pass

    def post_log(self, log_dir, log_level, log_msg):
        self.log.post_log(LogEvent(None, log_dir, log_level, log_msg))
        pass

    def post_data(self, data_dir, data):
        self.log.post_data(DataEvent(None, data_dir, data))
        pass
    # ----------------------------------------------------


if __name__ == '__main__':
    runtime = StationRuntime()

    runtime.stations[0] = runtime
    runtime.stations[1] = Station(1, 'station1', runtime)
    runtime.stations[2] = Station(1, 'station1', runtime)
    runtime.stations[3] = Station(1, 'station1', runtime)

    print(runtime)
