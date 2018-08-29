# -*- coding: utf-8 -*-

# !/usr/bin/env python3


# 输入信号
class Di(object):

    def __init__(self, driver, actid, name):
        self._driver = driver
        self.actid = actid
        self.name = name
        self.status = 0
        self.pls = 0
        self.plf = 0

    def set(self, sts):
        ret = self._driver.setdi(self.actid, sts)
        return ret

    def get(self):
        self.status = self._driver.getdi(self.actid)
        return self.status

    def check(self, sts):
        return self.status == sts

    def update(self):
        self.get()

    def __str__(self):
        return 'Di %s %s %s' %(self.actid, self.name, self.status)


# 输出信号
class Do(object):

    def __init__(self, driver, actid, name):
        self._driver = driver
        self.actid = actid
        self.name = name
        self.status = 0
        self.pls = 0
        self.plf = 0

    def set(self, sts):
        ret = self._driver.setdo(self.actid, sts)
        return ret

    def get(self):
        self.status = self._driver.getdo(self.actid)
        return self.status

    def check(self, sts):
        return self.status == sts

    def update(self):
        self.get()

    def __str__(self):
        return 'Do %s %s %s' %(self.actid, self.name, self.status)


# 虚拟IO信号
class Vio(Di):

    def __str__(self):
        return 'Vio %s %s %s' % (self.actid, self.name, self.status)


if __name__ == '__main__':
    pass
