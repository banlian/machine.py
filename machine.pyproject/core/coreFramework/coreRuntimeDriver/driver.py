# -*- coding: utf-8 -*-

# !/usr/bin/env python3


from core.coreDriver.cardDriver import *


class BaseDriver(object):

    def initialize(self, *args):
        pass

    def terminate(self):
        pass

    def update(self):
        pass


class GpioDriver(BaseDriver):

    def __init__(self, card_driver, actid, name):
        self.card_driver = card_driver
        self.actid = actid
        self.name = name

        self.di = []
        self.do = []

    def initialize(self, *args):
        self.card_driver.initialize(self.actid, args)
        self.di = [0 for i in range(len(self.card_driver.di))]
        self.do = [0 for i in range(len(self.card_driver.di))]

    def terminate(self):
        self.card_driver.terminate(self.actid)

    def update(self):
        self.card_driver.update()
        for i in range(len(self.card_driver.di)):
            self.di[i] = self.card_driver.di[i]
        for i in range(len(self.card_driver.do)):
            self.do[i] = self.card_driver.do[i]

    def setdi(self, index, status):
        return self.card_driver.setdi(self.actid, index, status)

    def getdi(self, index):
        return self.card_driver.getdi(self.actid, index)

    def setdo(self, index, status):
        return self.card_driver.setdo(self.actid, index, status)

    def getdo(self, index):
        return self.card_driver.getdo(self.actid, index)

    def __str__(self):
        return 'Driver:%s Name:%s Di:%s Do:%s' % (self.actid, self.name, len(self.di), len(self.do))


class AxisDriver(GpioDriver):

    def __init__(self, card_driver, actid, name):
        super().__init__(card_driver, actid, name)
        self.axis_status = []
        pass

    def initialize(self, *args):
        super().initialize(args)
        self.axis_status = [AxisStatus() for i in range(len(self.card_driver.axis_status))]

    def update(self):
        super().update()
        self.axis_status = [a for a in self.card_driver.axis_status]

    def clear(self, axis):
        return self.card_driver.clear(self.actid, axis)

    def clear_alarm(self, axis):
        return self.card_driver.clear_alarm(self.actid, axis)

    def set_servo(self, axis, enable):
        return self.card_driver.set_servo(self.actid, axis, enable)

    def get_motion_io(self, axis, io_status):
        io_status = self.card_driver.get_motion_io(self.actid, axis)

    def get_motion_status(self, axis, status):
        status = self.card_driver.get_motion_status(self.actid, axis)

    def set_enc_pos(self, axis, pos):
        return self.card_driver.set_enc_pos(self.actid, axis, pos)

    def get_enc_pos(self, axis):
        return self.card_driver.get_enc_pos(self.actid, axis)

    def set_cmd_pos(self, axis, pos):
        return self.card_driver.set_cmd_pos(self.actid, axis, pos)

    def get_cmd_pos(self, axis):
        return self.card_driver.get_cmd_pos(self.actid, axis)

    def zero_pos(self, axis):
        return self.card_driver.zero_pos(self.actid, axis)

    def set_axis_bandwidth(self, axis, bandwidth, us):
        return self.card_driver.set_axis_bandwidth(self.actid, axis, bandwidth, us)

    def set_move_params(self, axis, acc, dec, *args):
        return self.card_driver.set_move_params(self.actid, axis, acc, dec)

    def moveabs(self, axis, pos, vel):
        return self.card_driver.moveabs(self.actid, axis, pos, vel)

    def moverel(self, axis, step, vel):
        return self.card_driver.moverel(self.actid, axis, step, vel)

    def movestop(self, axis):
        return self.card_driver.movestop(self.actid, axis)

    def emg_stop(self, axis):
        return self.card_driver.emg_stop(self.actid, axis)

    def home_move(self, axis, vel):
        return self.card_driver.home_move(self.actid, axis)

    def set_home_capture(self, axis):
        return self.card_driver.set_home_capture(self.actid, axis)

    def get_home_capture(self, axis):
        return self.card_driver.get_home_capture(self.actid, axis)

    def set_index_capture(self, axis):
        return self.card_driver.set_index_capture(self.actid, axis)

    def get_index_capture(self, axis):
        return self.card_driver.get_index_capture(self.actid, axis)

    def __str__(self):
        return 'Driver:%s Name:%s Di:%s Do:%s Axis:%s' % (self.actid, self.name, len(self.di), len(self.do), len(self.axis_status))


if __name__ == '__main__':
    axis_driver = AxisDriver(None, 1, 'testDriver')

    print(axis_driver.__str__())
