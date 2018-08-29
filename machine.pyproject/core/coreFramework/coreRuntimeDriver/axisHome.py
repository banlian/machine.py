# -*- coding: utf-8 -*-

# !/usr/bin/env python3

import sys,os

class BaseHomeStragety(object):

    def homing(self, axis):
        pass

    def search_home_offset(self, axis):
        direction = axis.home_settings['home_dir']
        axis.home_state = 'wait_home_offset'
        return axis.moverel(-direction * axis.home_settings['search_home_len'] / 5, axis.home_settings['high_search_vel'])

    def search_limit(self, axis, next_state):
        if axis.mel and axis.home_settings['home_dir'] == -1:
            axis.home_state = next_state
            return 0
        if axis.pel and axis.home_settings['home_dir'] == 1:
            axis.home_state = next_state
            return 0
        direction = axis.home_settings['home_dir']
        axis.home_state = 'wait_move_limit'
        return axis.moverel(direction * axis.home_settings['search_limit_len'], axis.home_settings['high_search_vel'])

    def search_home(self, axis):
        if axis.org:
            return -1
        direction = axis.home_settings['home_dir']
        axis.home_state = 'wait_search_home'
        axis.set_home_capture()
        return axis.moverel(-direction * axis.home_settings['search_home_len'], axis.home_settings['low_search_vel'])

    def search_index(self, axis):
        if axis.index:
            return -1
        direction = axis.home_settings['home_dir']
        axis.home_state = 'wait_search_index'
        axis.set_home_capture()
        return axis.moverel(-direction * axis.home_settings['search_home_len'], axis.home_settings['low_search_vel'])

    def move_capture_pos(self, axis):
        axis.home_state = 'wait_move_capture_pos'
        return axis.moveabs(axis.home_capture_pos, axis.home_settings['low_search_vel'])

    def wait_home_offset(self, axis):
        if axis.mdn:
            axis.home_state = 'check_home'
            return axis.movestop()
        return 0

    def wait_move_limit(self, axis, next_state):
        if axis.mdn:
            if axis.mel or axis.pel:
                axis.home_state = next_state
        return 0

    def wait_search_home(self, axis, next_state):
        ret = axis.get_home_capture()
        if ret[1] == 1:
            axis.movestop()
            axis.home_capture_pos = ret[0]
            axis.home_capture_status = ret[1]
            axis.home_state = next_state
        return 0

    def wait_search_index(self, axis, next_state):
        ret = axis.get_index_capture()
        if ret[1] == 1:
            axis.movestop()
            axis.home_capture_pos = ret[0]
            axis.home_capture_status = ret[1]
            axis.home_state = next_state
        return 0

    def wait_move_done(self, axis):
        ret = 0
        if axis.mdn:
            ret = axis.zero_pos()
            axis.home_state = 'step_done'
            if axis.astp:
                return -1
        return ret


class HomeStrategy(BaseHomeStragety):
    def homing(self, axis):
        try:
            ret = 0
            if axis.home_state == 'move_limit':
                ret = self.search_limit(axis, 'search_home')
            elif axis.home_state == 'wait_move_limit':
                ret = self.wait_move_limit(axis, 'search_home')
            elif axis.home_state == 'search_home':
                ret = self.search_home(axis)
            elif axis.home_state == 'wait_search_home':
                ret = self.wait_search_home(axis, 'move_capture_pos')
            elif axis.home_state == 'move_capture_pos':
                ret = self.move_capture_pos(axis)
            elif axis.home_state == 'wait_move_capture_pos':
                ret = self.wait_move_done(axis)
            else:
                return -1
            return ret
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

class HomeIndexStrategy(BaseHomeStragety):
    def homing(self, axis):
        ret = 0
        if axis.home_state == 'move_limit':
            ret = self.search_limit(axis, 'search_home')
        elif axis.home_state == 'wait_move_limit':
            ret = self.wait_move_limit(axis, 'search_home')
        elif axis.home_state == 'search_home':
            ret = self.search_home(axis)
        elif axis.home_state == 'wait_search_home':
            ret = self.wait_search_home(axis, 'search_index')
        elif axis.home_state == 'search_index':
            ret = self.search_index(axis)
        elif axis.home_state == 'wait_search_index':
            ret = self.wait_search_index(axis, 'move_capture_pos')
        elif axis.home_state == 'move_capture_pos':
            ret = self.move_capture_pos(axis)
        elif axis.home_state == 'wait_move_capture_pos':
            ret = self.wait_move_done(axis)
        else:
            return -1
        return ret


class HomeMgr(object):

    def __init__(self):
        self._strageties = {'home': HomeStrategy(),
                            'home_index': HomeIndexStrategy()}
        pass

    def homing(self, axis):
        if axis.home_settings['home_mode'] not in self._strageties.keys():
            return -1
        return self._strageties[axis.home_settings['home_mode']].homing(axis)
