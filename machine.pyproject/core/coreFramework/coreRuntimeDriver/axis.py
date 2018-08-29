# -*- coding: utf-8 -*-

# !/usr/bin/env python3


from core.coreFramework.coreRuntimeDriver.driver import *


class Axis(object):

    def __init__(self, driver, setid, actid, name, ratio, acc, dec, safe_check_lambda):
        self._driver = driver
        self._safe_check = safe_check_lambda
        self.setid = setid
        self.actid = actid
        self.name = name
        self._ratio = ratio
        self._acc = acc
        self._dec = dec
        self.curpos = 0
        self.encpos = 0
        self.cmdpos = 0

        self.home = False,
        self.home_state = 'none'
        self.home_capture_status = 0
        self.home_capture_pos = 0
        self.home_settings = {'home_mode': 'home',
                              'home_dir': -1,
                              'search_limit_len': 3000,
                              'search_home_len': 3000,
                              'low_search_vel': 10,
                              'high_search_vel': 100}

        self.emgency = False
        self.hmv = False
        self.astp = False
        self.mdn = False
        self.alarm = False
        self.pel = False
        self.mel = False
        self.org = False
        self.index = False,
        self.servo = False

    def __str__(self):
        return 'Axis %s %s %s %.3d %.3d %.3d' % (self.name, self.setid, self.actid, self._ratio, self._acc, self._dec)

    def update(self):
        axis_status = self._driver.axis_status[self.actid]
        self.encpos = axis_status.ENCPOS
        self.cmdpos = axis_status.CMDPOS
        self.astp = axis_status.ASTP
        self.hmv = axis_status.ISMOVE
        self.mdn = axis_status.MDN
        self.alarm = axis_status.ALARM
        self.pel = axis_status.PEL
        self.mel = axis_status.MEL
        self.org = axis_status.ORG
        self.index = axis_status.INDEX
        self.servo = axis_status.SERVO

    def clear(self):
        self._driver.clear(self.actid)
        pass

    def clear_alarm(self):
        return self._driver.clear_alarm(self.actid)

    def set_servo(self, enable):
        if not enable:
            self.home = False
        return self._driver.set_servo(self.actid, enable)

    def set_enc_pos(self, pos):
        return self._driver.set_enc_pos(self.actid, pos)

    def get_enc_pos(self):
        self.encpos = self._driver.get_enc_pos(self.actid)
        return self.encpos

    def set_cmd_pos(self, pos):
        return self._driver.set_cmd_pos(self.actid, pos)

    def get_cmd_pos(self):
        self.cmdpos = self._driver.get_cmd_pos(self.actid)
        return self.cmdpos

    def zero_pos(self):
        self.encpos = 0
        return self._driver.zero_pos(self.actid)

    def set_axis_bandwidth(self, bandwidth, us):
        return self._driver.set_axis_bandwidth(self.actid, bandwidth, us)

    def set_move_params(self, acc, dec):
        return self._driver.set_move_params(self.actid, acc, dec)

    def moveabs(self, pos, vel):
        return self._driver.moveabs(self.actid, pos, vel)

    def moverel(self, step, vel):
        return self._driver.moverel(self.actid, step, vel)

    def movestop(self):
        return self._driver.movestop(self.actid)

    def emg_stop(self):
        return self._driver.emg_stop(self.actid)

    def home_move(self, axis, timeout):
        return self._driver.home_move(self.actid, timeout)

    def set_home_capture(self):
        return self._driver.set_home_capture(self.actid)

    def get_home_capture(self):
        capture = self._driver.get_home_capture(self.actid)
        if capture[1] == 1:
            self.home_capture_pos = capture[0]
            self.home_capture_status = capture[1]
        return capture

    def set_index_capture(self):
        return self._driver.set_index_capture(self.actid)

    def get_index_capture(self):
        capture = self._driver.get_index_capture(self.actid)
        if capture[1] == 1:
            self.home_capture_pos = capture[0]
            self.home_capture_status = capture[1]
        return capture
