# -*- coding: utf-8 -*-

# !/usr/bin/env python3

from core.coreFramework.coreEvents.eventServer import EventServer
from core.coreFramework.stationTask import StationTask

from core.coreFramework.coreRuntime.alarmEventHandler import SystemAlarm,AlarmEvent,Alarm2ViewEventHandler


class Alarm(StationTask):

    def __init__(self):
        self.alarms = {
            SystemAlarm.ESTOP: '急停按下',
            SystemAlarm.DOOR_OPEN: '安全门打开',
            SystemAlarm.SAFECURTAIN_ACT: '安全光栅触发',

            SystemAlarm.AXIS_SRVON_FAIL: '轴使能失败',
            SystemAlarm.AXIS_HOME_ERR: '轴回原点异常',
            SystemAlarm.AXIS_HOME_FAIL: '轴回原点失败',
            SystemAlarm.AXIS_MOVE_FAIL: '轴移动异常',
            SystemAlarm.AXIS_ASTP: '轴异常停止',
            SystemAlarm.AXIS_ALM: '轴报警',
            SystemAlarm.AXIS_PEL: '轴正限位触发',
            SystemAlarm.AXIS_MEL: '轴负限位触发',
            SystemAlarm.AXIS_PLS_ERR: '轴误差异常',

            SystemAlarm.DO_ERROR: 'DO异常',
            SystemAlarm.VIO_ERROR: 'VIO异常',
            SystemAlarm.DI_TIMEOUT: '等待DI信号超时',
            SystemAlarm.VIO_TIMEOUT: '等待VIO信号超时',

            SystemAlarm.DRIVER_INIT_FAIL: '驱动初始化异常',
            SystemAlarm.DRIVER_LOAD_PARAMS_FAIL: '驱动加载参数异常', }

        self.event_server = EventServer('alarm')
        self.event_handlers = {'view': Alarm2ViewEventHandler()}

        super().__init__(-1, 'alarm', None)

    def start(self):
        # init alarm view components
        super().start()

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

    def post_event(self, event):
        for handler in self.event_handlers.values():
            self.event_server.post(AlarmEvent(handler, event.station, event.alarm_level, event.alarm_id, event.alarm_msg))

    def register(self, index, alarm_info):
        self.alarms[index] = alarm_info

    def unregister(self, index):
        del self.alarms[index]


if __name__ == '__main__':
    a = {1: 'test', 2: 'test2'}
    print(a.values())

    alarm = Alarm()
    print(alarm.alarms)
