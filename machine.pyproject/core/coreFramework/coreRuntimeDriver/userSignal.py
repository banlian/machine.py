# -*- coding: utf-8 -*-

# !/usr/bin/env python3


from core.coreFramework.coreRuntimeDriver.gpio import *


class Signal(object):

    def __init__(self):
        self.status = 0

    def set(self, sts):
        self.status = sts

    def get(self):
        return self.status

    def update(self):
        pass


class Light(object):

    def __init__(self, do_red, do_green, do_yellow, do_beep):
        self.do_red = do_red,
        self.do_green = do_green
        self.do_yellow = do_yellow
        self.do_beep = do_beep
        self.state = 'manual'
        self.auto_state = 'waitreset'

    def yellow(self, sts):
        if sts == 0:
            self.do_yellow.set(0)
        elif sts == 1:
            self.do_yellow.set(1)
        elif sts == 2:
            self.do_yellow.set(1 if self.do_yellow.get() == 0 else 0)
        return self

    def red(self, sts):
        if sts == 0:
            self.do_red.set(0)
        elif sts == 1:
            self.do_red.set(1)
        elif sts == 2:
            self.do_red.set(1 if self.do_red.get() == 0 else 0)
        return self

    def green(self, sts):
        if sts == 0:
            self.do_green.set(0)
        elif sts == 1:
            self.do_green.set(1)
        elif sts == 2:
            self.do_green.set(1 if self.do_green.get() == 0 else 0)
        return self

    def beep(self, sts):
        if sts == 0:
            self.do_beep.set(0)
        elif sts == 1:
            self.do_beep.set(1)
        elif sts == 2:
            self.do_beep.set(1 if self.do_beep.get() == 0 else 0)
        return self

    def update(self):

        if self.state == 'estop':
            self.red(2).yellow(0).green(0).beep(2)
        elif self.state == 'error':
            self.red(2).yellow(0).green(0).beep(0)
        elif self.state == 'auto':
            if self.auto_state == 'waitreset':
                self.red(1).yellow(0).green(0).beep(0)
            elif self.auto_state == 'resetting':
                self.red(0).yellow(2).green(0).beep(0)
            elif self.auto_state == 'waitrun':
                self.red(0).yellow(1).green(0).beep(0)
            elif self.auto_state == 'running':
                self.red(0).yellow(0).green(1).beep(0)
            elif self.auto_state == 'pause':
                self.red(0).yellow(2).green(0).beep(0)
        else:
            self.red(0).yellow(1).green(0).beep(0)


if __name__ == '__main__':

    pass
