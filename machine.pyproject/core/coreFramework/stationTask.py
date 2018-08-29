# -*- coding: utf-8 -*-

# !/usr/bin/env python3


from threading import *
from core.coreFramework.coreEvents.userEventHandler import UserEventHandler
from core.coreFramework.coreRuntime.mainGpioHandler import SetDo,SetVio,WaitDi,WaitVio
from core.coreFramework.coreRuntime.mainMoveHandler import MoveEventHandler

from core.coreFramework.coreRuntime.alarmEventHandler import SystemAlarm

import sys,os

class StationTask(UserEventHandler):

    def __init__(self, setid, name, station):
        self.setid = setid
        self.name = name
        self.station = station
        self.event_handlers = {}

        self._thread = None
        self.is_running = False

    def set_station(self, station):
        self.station = station
        self.event_handlers['setdo'] = SetDo(self)
        self.event_handlers['setvio'] = SetVio(self)
        self.event_handlers['waitdi'] = WaitDi(self)
        self.event_handlers['waitvio'] = WaitVio(self)
        self.event_handlers['move'] = MoveEventHandler(self)

    def __str__(self):
        return 'Task %s %s' % (self.name, self.setid)

    # ------------------------ task handling events

    def handle_event(self, event):
        [handler.handle_event(event) for handler in self.event_handlers.values()]
        super().handle_event(event)

    def on_start(self, event):
        self.start()

    def on_stop(self, event):
        self.stop()

    def on_reset(self, event):
        self.reset()

    # ------------------------

    # -------------------------thread manage methods

    def start(self):
        """启动"""
        if self.is_running:
            return -1
        if self._thread is not None:
            return -1
        self.is_running = True
        # 启动事件处理线程
        self._thread = Thread(target=self._running)
        self._thread.setDaemon(True)
        self._thread.start()
        return 0

    def stop(self):
        """停止"""
        self.is_running = False
        # 等待事件处理线程退出
        if self._thread is not None:
            self._thread.join()
            self._thread = None
            return 0
        return -1

    def reset(self):
        """复位"""
        if self.is_running:
            return -1
        if self._thread is not None:
            return -1
        self.is_running = True
        self._thread = Thread(target=self._resetting)
        self._thread.setDaemon(True)
        self._thread.start()
        return 0

    def join(self):
        if not self.is_running:
            return -1
        if self._thread is None:
            return -1
        self._thread.join()
        return 0

    def _running(self):
        try:
            while self.is_running:
                if self.run_loop() != 0:
                    self.is_running = False
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            self.error(9999, str(self) + 'runnning cancelled')
        print('%s run loop finish' % self.name)

    def run_loop(self):
        pass

    def _resetting(self):
        try:
            while self.is_running:
                if self.reset_loop() != 0:
                    self.is_running = False
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            self.error(9999, str(self) + 'resetting cancelled')
        print('%s reset loop finish' % self.name)

    def reset_loop(self):
        pass

    # ----------------------------------

    # ------------------ set io methods

    def setdo(self, do, do_status):
        ret = self.event_handlers['setdo'].setio(do, do_status)
        if ret!=0:
            self.error(SystemAlarm.DO_ERROR, ','.join([setdo for setdo in do]))
        return ret

    def setvio(self, vio, vio_status):
        ret = self.event_handlers['setvio'].setio(vio, vio_status)
        if ret != 0:
            self.error(SystemAlarm.VIO_TIMEOUT, ','.join([setvio for setvio in vio]))
        return ret

    def waitdi(self, di, di_status, timeout, is_error):
        ret = self.event_handlers['waitdi'].waitio(di, di_status, timeout, is_error)
        if ret != 0:
            self.error(SystemAlarm.DI_TIMEOUT, ','.join([setdi for setdi in di]))
        return ret

    def waitvio(self, do, do_status, timeout, is_error = True):
        ret = self.event_handlers['waitvio'].waitio(do, do_status, timeout, is_error)
        if ret != 0:
            self.error(SystemAlarm.VIO_TIMEOUT, ','.join([setdo for setdo in do]))
        return ret

    # ------------------

    # ------------------ move methods
    def set_servo(self, axis, enable):
        ret = self.event_handlers['move'].servo(axis, enable)
        if ret != 0:
            self.error(SystemAlarm.AXIS_SRVON_FAIL, ','.join([a for a in axis]))
        return ret

    def movehome(self, axis, timeout):
        ret = self.event_handlers['move'].movehome(axis, timeout)
        if ret != 0:
            self.error(SystemAlarm.AXIS_HOME_FAIL, ','.join([a for a in axis]))
        return ret

    def moveabs(self, axis, pos, vel, timeout):
        ret = self.event_handlers['move'].moveabs(axis, pos, vel, timeout)
        if ret != 0:
            self.error(SystemAlarm.AXIS_MOVE_FAIL, ','.join([a for a in axis]))
        return ret

    def moverel(self, axis, step, vel, timeout):
        ret = self.event_handlers['move'].moverel(axis, step, vel, timeout)
        if ret != 0:
            self.error(SystemAlarm.AXIS_MOVE_FAIL, ','.join([a for a in axis]))
        return ret

    def moveabs2stop(self, axis, pos, vel, stop_di, stop_status, timeout):
        ret = self.event_handlers['move'].moveabs2stop(axis, pos, vel, stop_di, stop_status, timeout)
        if ret != 0:
            self.error(SystemAlarm.AXIS_MOVE_FAIL, ','.join([a for a in axis]))
        return ret

    def moverel2stop(self, axis, step, vel, stop_di, stop_status, timeout):
        ret = self.event_handlers['move'].moverel2stop(axis, step, vel, stop_di, stop_status, timeout)
        if ret != 0:
            self.error(SystemAlarm.AXIS_MOVE_FAIL, ','.join([a for a in axis]))
        return ret

    def moveabs2trigger(self, axis, pos, vel, pos_compare_dir, pos_compare_pos, pos_compare_trigger_event, timeout):
        ret = self.event_handlers['move'].moveabs2trigger(axis, pos, vel, pos_compare_dir, pos_compare_pos, pos_compare_trigger_event, timeout)
        if ret != 0:
            self.error(SystemAlarm.AXIS_MOVE_FAIL, ','.join([a for a in axis]))
        return ret

    def moverel2trigger(self, axis, step, vel, pos_compare_dir, pos_compare_pos, pos_compare_trigger_event, timeout):
        ret = self.event_handlers['move'].moverel2trigger(axis, step, vel, pos_compare_dir, pos_compare_pos, pos_compare_trigger_event, timeout)
        if ret != 0:
            self.error(SystemAlarm.AXIS_MOVE_FAIL, ','.join([a for a in axis]))
        return ret

    # ------------------

    # ----------------------------- move async methods

    def wait_move_done(self, timeout):
        return self.event_handlers['move'].wait_event_done(timeout)

    # ------------------------------

    # ----------------- alarm/log/data methods

    def error(self, id, msg):
        self.station.post_alarm(self.station, 'error', id, msg)
        self.log('%s_%s' % (self.station.name, self.name),  'error', msg)

    def warning(self, id, msg):
        self.station.post_alarm(self.station, 'warning', id, msg)
        self.log('%s_%s' % (self.station.name, self.name), 'warning', msg)

    def log(self, log_dir, log_level, log_msg):
        self.station.post_log(log_dir, log_level, log_msg)

    def info(self, log_msg):
        self.log('%s_%s' % (self.station.name, self.name), 'info', log_msg)

    def debug(self, log_msg):
        self.log('%s_%s' % (self.station.name, self.name), 'debug', log_msg)

    def trace(self, log_msg):
        self.log('%s_%s' % (self.station.name, self.name), 'trace', log_msg)

    def data(self, data_dir, data):
        self.station.post_data(data_dir, data)

    # ----------------------------------------
