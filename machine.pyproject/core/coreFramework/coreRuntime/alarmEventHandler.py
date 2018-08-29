# -*- coding: utf-8 -*-

# !/usr/bin/env python3


from core.coreFramework.coreEvents.userEvent import UserEvent
from core.coreFramework.coreEvents.userEventHandler import UserEventHandler,UserEventType
from enum import Enum
import datetime

from PyQt5.QtWidgets import QApplication, QWidget


class AlarmEvent(UserEvent):

    def __init__(self, event_handler, station, level, alarm_id, alarm_msg):
        self.datetime = datetime.datetime.now()
        self.station = station
        self.alarm_level = level
        self.alarm_id = alarm_id
        self.alarm_msg = alarm_msg
        super().__init__(event_handler, UserEventType.ALARM)


class SystemAlarm(Enum):
    ESTOP = 0
    DOOR_OPEN = 1
    SAFECURTAIN_ACT = 2

    AXIS_SRVON_FAIL = 100
    AXIS_HOME_FAIL = 101
    AXIS_HOME_ERR = 102
    AXIS_MOVE_FAIL = 103
    AXIS_ASTP = 104
    AXIS_ALM = 105
    AXIS_PEL = 106
    AXIS_MEL = 107
    AXIS_PLS_ERR = 108

    DO_ERROR = 200
    VIO_ERROR = 201
    DI_TIMEOUT = 202
    VIO_TIMEOUT = 203

    DRIVER_INIT_FAIL = 300
    DRIVER_LOAD_PARAMS_FAIL = 301


class Alarm2ViewEventHandler(UserEventHandler):

    def __init__(self):
        # self.alarm_view = AlarmView()
        super().__init__()

    def on_user_event(self, event):
        if event.type == UserEventType.ALARM:
            # show alarm msg
            # self.alarm_view.show_alarm(event)
            pass

    def initialize(self):
        pass

    def terminate(self):
        # self.alarm_view.close()
        pass


class AlarmView(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('报警信息')
        self.resize(600, 400)
        self.move(300, 300)
        self.show()

    def show_alarm(self, alarmEvent):
        self.show()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = AlarmView()
    sys.exit(app.exec_())
