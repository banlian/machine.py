# -*- coding: utf-8 -*-

# !/usr/bin/env python3


from core.coreDriver.cardDriver import CardDriver
from threading import RLock


class VirtualAxisCard(CardDriver):

    def __init__(self):
        super().__init__()
        self._io_num = 128
        self._axis_num = 32

    def initialize(self, actid, *args):
        super().initialize(actid, args)
        return 0

    def terminate(self, actid):
        return 0

    def load_params(self, actid, *args):
        return 0

    def setdi(self, actid, index, sts):
        self.di[index] = sts
        return 0

    def getdi(self, actid, index):
        return self.di[index]

    def setdo(self, actid, index, sts):
        self.do[index] = sts
        return 0

    def getdo(self, actid, index):
        return self.do[index]

    def set_servo(self, actid, index, servo):
        self.axis_status[index].SERVO = True
        return 0

    def set_enc_pos(self, actid, index, pos):
        self.axis_status[index].ENCPOS = pos
        return 0

    def get_enc_pos(self, actid, index):
        return self.axis_status[index].ENCPOS

    def set_cmd_pos(self, actid, index, pos):
        self.axis_status[index].CMDPOS = pos
        return 0

    def get_cmd_pos(self, actid, index):
        return self.axis_status[index].CMDPOS

    def zero_pos(self, actid, index):
        self.axis_status[index].ENCPOS = 0
        self.axis_status[index].CMDPOS = 0
        return 0

    def set_home_capture(self, actid, index):
        self.axis_status[index].ISCAPTUREHOME = True
        return 0

    def get_home_capture(self, actid, index):
        return self.axis_status[index].ENCPOS, 1 if self.axis_status[index].ORG else 0

    def set_index_capture(self, actid, index):
        self.axis_status[index].ISCAPTUREINDEX = True
        return 0

    def get_index_capture(self, actid, index):
        return self.axis_status[index].ENCPOS, 1 if self.axis_status[index].INDEX else 0

    def moveabs(self, actid, index, pos, vel, acc=1000, dec=1000):
        self.axis_status[index].MDN = False
        self.axis_status[index].CMDPOS = pos

        direction = 1 if self.axis_status[index].ENCPOS <= self.axis_status[index].CMDPOS else -1

        self.axis_status[index].VEL = abs(vel) * direction
        self.axis_status[index].ACC = acc
        self.axis_status[index].DEC = dec
        self.axis_status[index].ISMOVE = True
        return 0

    def moverel(self, actid, index, step, vel, acc=1000, dec=1000):
        self.axis_status[index].MDN = False
        self.axis_status[index].CMDPOS = self.axis_status[index].ENCPOS + step

        direction = 1 if self.axis_status[index].ENCPOS <= self.axis_status[index].CMDPOS else -1

        self.axis_status[index].VEL = abs(vel) * direction
        self.axis_status[index].ACC = acc
        self.axis_status[index].DEC = dec
        self.axis_status[index].ISMOVE = True
        return 0

    def movestop(self, actid, index):
        self.axis_status[index].MDN = True
        self.axis_status[index].ISMOVE = False
        return 0

    def update(self):
        for a in self.axis_status:
            a.update()
        return 0


class VIOCard(CardDriver):

    def __init__(self):
        super().__init__()
        self._io_num = 1024
        self._axis_num = 0
        self.rlock1 = RLock()
        self.rlock2 = RLock()

    def initialize(self, actid, *args):
        super().initialize(actid, args)
        pass

    def terminate(self, actid):
        pass

    def load_params(self, actid, *args):
        pass

    def setdi(self, actid, index, sts):
        self.rlock1.acquire()
        self.di[index] = sts
        self.rlock1.release()

    def getdi(self, actid, index):
        return self.di[index]

    def setdo(self, actid, index, sts):
        self.rlock2.acquire()
        self.do[index] = sts
        self.rlock2.release()

    def getdo(self, actid, index):
        return self.do[index]


if __name__ == '__main__':
    vc = VirtualAxisCard()
    vc.initialize(0, 'test')

    vc.setdi(0, 0, 1)
    vc.setdi(0, 1, 1)

    vc.update()

    print(vc.di)
    print(vc.axis_status)
