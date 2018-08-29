# -*- coding: utf-8 -*-

# !/usr/bin/env python3
'''
created on 2018-01-16

@author: zzz
'''

from core.coreDriver.cardDriver import CardDriver
from core.coreDriver.gts.gts import Gts


class Gts800Card(CardDriver):

    def __init__(self):
        super().__init__()
        self.__gts = Gts()
        self._io_num = 32
        self._axis_num = 8

    def initialize(self, actid, *args):
        super().initialize(actid, args)
        return self.__gts.open(actid)

    def terminate(self, actid):
        return self.__gts.close(actid)

    def load_params(self, id, *args):
        return self.__gts.load_params(id, args[0])

    def update(self):
        pass;


if __name__ == '__main__':
    gts = Gts800Card()
    ret = gts.initialize(0)
    print(ret)
