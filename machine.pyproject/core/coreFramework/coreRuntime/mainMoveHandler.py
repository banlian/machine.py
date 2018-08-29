# -*- coding: utf-8 -*-

# !/usr/bin/env python3

from core.coreFramework.coreEvents.userEventHandler import *
from core.coreFramework.coreRuntime.mainEventHandler import *

from core.coreFramework.coreRuntime.alarmEventHandler import *
from core.coreFramework.coreRuntimeDriver.axis import *
from core.coreFramework.coreRuntimeDriver.axisHome import *


class MotionBaseHandler(MainEventHandler):

    def __init__(self, task):
        self._home_mgr = HomeMgr()
        self.mode = None
        self.axis = []
        self.enable = []
        self.timeout = 0
        super().__init__(task)

    def on_event_handle(self, event):
        if event.event_type == UserEventType.AXISSERVO:
            self._start_tick = self.task.station.runtime.time_ticks
            ret = [self.axis[i].set_servo(self.enable[i]) for i in range(len(self.axis))]
            if any(ret):
                self.task.error(SystemAlarm.AXIS_SRVON_FAIL, ','.join([a.name for a in self.axis]))
            return 0
        elif event.event_type == UserEventType.AXISHOME:
            for a in self.axis:
                a.home = False
                a.home_state = 'move_limit'
                a.home_capture_pos = 0
                a.home_capture_status = 0
            return 0
        # change handler state by super class
        return super().on_event_handle(event)

    def on_event_handling(self):
        if self.mode == 'servo':
            ret = [a.servo for a in self.axis]
            if all(ret):
                self.state = 'done'
            elif self.task.station.runtime.time_ticks - self._start_tick > self.timeout:
                self.task.error(SystemAlarm.AXIS_SRVON_FAIL, ','.join([a.name for a in self.axis]))
                self.state = 'timeout'
        elif self.mode == 'home':
            ret = [self._home_mgr.homing(a) for a in self.axis]
            if any(ret):
                self.task.error(SystemAlarm.AXIS_HOME_ERR, ','.join([a.name for a in self.axis]))
            if all(a.home_state == 'step_done' for a in self.axis):
                for a in self.axis:
                    a.home = True
                self.state = 'done'

        # axis safe status check
        ret = [a.astp or a.alarm for a in self.axis]
        if any(ret):
            [a.movestop() for a in self.axis]
            self.task.error(SystemAlarm.AXIS_ASTP, ','.join([a.name for a in self.axis]))
            self.state = 'error'

    def servo(self, axis, enable):
        self.mode = 'servo'
        self.axis = [self.task.station.runtime.axis[a] for a in axis]
        self.enable = enable
        self.timeout = 3000
        self.post_event(UserEventType.AXISSERVO)
        return self.wait_event_done(3000)

    def movehome(self, axis, timeout):
        self.mode = 'home'
        self.axis = [self.task.station.runtime.axis[a] for a in axis]
        self.timeout = timeout
        self.post_event(UserEventType.AXISHOME)
        return self.wait_event_done(timeout)

    def movehome_async(self, axis):
        self.mode = 'home'
        self.axis = [self.task.station.runtime.axis[a] for a in axis]
        self.post_event(UserEventType.AXISHOME)


class MoveEventHandler(MotionBaseHandler):

    def __init__(self, task):
        self.task = task
        self.axis = []
        self.mode = 'None'
        self.pos = []
        self.step = []
        self.vel = []

        self.stop_axis = []
        self.stop_di = []
        self.stop_di_status = []
        self.is_stop_trigger = False

        self.stop_condition = None
        self.is_stop_condition_trigger = False

        self.pos_compare_axis = []
        self.pos_compare_pos = []
        self.pos_compare_dir = []
        self.pos_compare_trigger_event = None

        self.compare_trigger_condition = None
        self.compare_trigger_event = None

        super().__init__(task)

    def on_stop(self, event):
        [a.movestop() for a in self.axis if a is Axis]
        super().on_stop(event)

    def on_pause(self, event):
        [a.movestop() for a in self.axis if a is Axis]
        super().on_pause(event)

    def on_event_handle(self, event):
        if event.event_type == UserEventType.AXISMOVE:
            if self.mode == 'moveabs' or self.mode.startswith('moveabs'):
                ret = [self.axis[i].absmove(self.pos[i], self.vel[i]) for i in range(len(self.axis))]
                if any(ret):
                    self.task.error(SystemAlarm.AXIS_MOVE_FAIL, ','.join([a.name for a in self.axis]))
            elif self.mode == 'moverel' or self.mode.startswith('moverel'):
                ret = [self.axis[i].relmove(self.step[i], self.vel[i]) for i in range(len(self.axis))]
                if any(ret):
                    self.task.error(SystemAlarm.AXIS_MOVE_FAIL, ','.join([a.name for a in self.axis]))
            return 0
        else:
            return super().on_event_handle(event)

    def on_event_handling(self):
        super().on_event_handling()

        if self.mode == 'moveabs' or self.mode == 'moverel':
            ret = [a.mdn for a in self.axis]
            if all(ret):
                self.state = 'done'
        elif self.mode == 'moveabs2stop' or self.mode == 'moverel2stop':
            ret = [self.stop_di[i].check(self.stop_di_status[i]) for i in range(len(self.stop_di))]
            if all(ret):
                [a.movestop() for a in self.stop_axis]
            elif self.task.station.runtime.time_ticks - self._start_tick > self.timeout:
                [a.movestop() for a in self.stop_axis]
                self.task.error(SystemAlarm.AXIS_MOVE_FAIL, ','.join([a.name for a in self.axis]))
                self.state = 'timeout'
            pass
        elif self.mode == 'moveabs2trigger' or self.mode == 'moverel2trigger':
            # check trigger
            if self.pos_compare_trigger_event is not None:
                ret = [self.pos_compare_axis[i].curpos < self.pos_compare_pos[i] if self.pos_compare_dir[i] < 0 else self.pos_compare_axis[i].curpos > self.pos_compare_pos[i] for i in range(len(self.pos_compare_axis))]
                if all(ret):
                    # todo to define trigger mechanism
                    self.pos_compare_trigger_event.action()
                    self.pos_compare_trigger_event = None
            # check mdn
            ret = [a.mdn for a in self.axis]
            if all(ret):
                self.state = 'done'
        elif self.mode == 'moveabs2stop_fun' or self.mode == 'moverel2stop_fun':
            pass
        elif self.mode == 'moveabs2trigger_fun' or self.mode == 'moverel2trigger_fun':

            ret = [a.mdn for a in self.axis]
            if all(ret):
                self.state = 'done'
        pass

    def move_abs(self, axis, pos, vel, timeout):
        self.mode = 'moveabs'
        self.axis = [self.task.station.runtime.axis[a] for a in axis]
        self.pos = pos
        self.vel = vel
        self.timeout = timeout
        self.post_event(UserEventType.AXISMOVE)
        return self.wait_event_done(timeout)

    def move_abs_async(self, axis, pos, vel):
        self.mode = 'moveabs'
        self.axis = [self.task.station.runtime.axis[a] for a in axis]
        self.pos = pos
        self.vel = vel
        self.post_event(UserEventType.AXISMOVE)
        return 0

    def move_rel(self, axis, step, vel, timeout):
        self.mode = 'moverel'
        self.axis = [self.task.station.runtime.axis[a] for a in axis]
        self.step = step
        self.vel = vel
        self.timeout = timeout
        self.post_event(UserEventType.AXISMOVE)
        return self.wait_event_done(timeout)

    def move_rel_async(self, axis, step, vel):
        self.mode = 'moverel'
        self.axis = [self.task.station.runtime.axis[a] for a in axis]
        self.step = step
        self.vel = vel
        self.post_event(UserEventType.AXISMOVE)
        return 0

    def moveabs2stop(self, axis, pos, vel, stop_di, stop_status, timeout):
        self.mode = 'moveabs2stop'
        self.axis = [self.task.station.runtime.axis[a] for a in axis]
        self.pos = pos
        self.vel = vel
        self.stop_axis = axis
        self.stop_di = stop_di
        self.stop_di_status = stop_status
        self.is_stop_trigger = False
        self.timeout = timeout
        self.post_event(UserEventType.AXISMOVE)
        ret = self.wait_event_done(timeout)
        return ret, self.is_stop_trigger

    def moverel2stop(self, axis, step, vel, stop_di, stop_status, timeout):
        self.mode = 'moverel2stop'
        self.axis = [self.task.station.runtime.axis[a] for a in axis]
        self.step = step
        self.vel = vel
        self.stop_axis = axis
        self.stop_di = stop_di
        self.stop_di_status = stop_status
        self.is_stop_trigger = False
        self.timeout = timeout
        self.post_event(UserEventType.AXISMOVE)
        ret = self.wait_event_done(timeout)
        return ret, self.is_stop_trigger

    def moveabs2trigger(self, axis, pos, vel, pos_compare_dir, pos_compare_pos, pos_compare_trigger_event, timeout):
        self.mode = 'moveabs2trigger'
        self.axis = [self.task.station.runtime.axis[a] for a in axis]
        self.pos = pos
        self.vel = vel
        self.pos_compare_axis = self.axis
        self.pos_compare_dir = pos_compare_dir
        self.pos_compare_pos = pos_compare_pos
        self.pos_compare_trigger_event = pos_compare_trigger_event
        self.timeout = timeout
        self.post_event(UserEventType.AXISMOVE)
        return self.wait_event_done(timeout)

    def moverel2trigger(self, axis, step, vel, pos_compare_dir, pos_compare_pos, pos_compare_trigger_event, timeout):
        self.mode = 'moverel2trigger'
        self.axis = [self.task.station.runtime.axis[a] for a in axis]
        self.step = step
        self.vel = vel
        self.pos_compare_axis = self.axis
        self.pos_compare_dir = pos_compare_dir
        self.pos_compare_pos = pos_compare_pos
        self.pos_compare_trigger_event = pos_compare_trigger_event
        self.timeout = timeout
        self.post_event(UserEventType.AXISMOVE)
        return self.wait_event_done(timeout)