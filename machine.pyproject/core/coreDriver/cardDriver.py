# -*- coding: utf-8 -*-

# !/usr/bin/env python3

' CardDriver module '

__author__ = 'zzz'


class CardDriver(object):

    def __init__(self):
        self._io_num = 0
        self.di = []
        self.do = []
        self._axis_num = 0
        self.axis_status = []

    def initialize(self, actid, *args):
        self.di = [0 for i in range(self._io_num)]
        self.do = [0 for i in range(self._io_num)]
        self.axis_status = [AxisStatus() for i in range(self._axis_num)]
        pass

    def terminate(self, actid):
        pass

    def load_params(self, actid, *args):
        pass

    # ---------------------------------------io methods
    def setdi(self, actid, index, sts):
        pass

    def getdi(self, actid, index):
        pass

    def setdo(self, actid, index, sts):
        pass

    def getdo(self, actid, index):
        pass

    # ------------------------------------------axis methods
    def set_servo(self, actid, index, servo):
        pass

    def set_axis_bandwactidth(self, actid, index, bandwactidth):
        pass

    def set_enc_pos(self, actid, index, pos):
        pass

    def get_enc_pos(self, actid, index):
        pass

    def set_cmd_pos(self, actid, index, pos):
        pass

    def get_cmd_pos(self, actid, index):
        pass

    def zero_pos(self, actid, index):
        pass

    def moveabs(self, actid, index, pos, vel, acc, dec):
        pass

    def moverel(self, actid, index, step, vel, acc, dec):
        pass

    def movestop(self, actid, index):
        pass

    def emg_stop(self, actid, index):
        pass

    # ----------------------------------------- home methods
    def home_move(self, actid, index):
        pass

    def set_home_capture(self, actid, index):
        pass

    def get_home_capture(self, actid, index):
        pass

    def set_index_capture(self, actid, index):
        pass

    def get_index_capture(self, actid, index):
        pass

    def update(self):
        pass


class AxisStatus(object):
    PEL_LIM = 20000
    MEL_LIM = -300
    ORG_LIM = 111
    INDEX_LIM = 500

    def __init__(self):
        self.SERVO = False
        self.ALARM = False
        self.ASTP = False
        self.MDN = False

        self.MEL = False
        self.PEL = False
        self.ORG = False
        self.INDEX = False

        self.ISMOVE = False

        self.ENCPOS = 0
        self.CMDPOS = 0
        self.VEL = 1
        self.ACC = 1
        self.DEC = 1

        self.ISCAPTUREHOME = False
        self.ISCAPTUREINDEX = False

    def update(self):
        if self.ISMOVE and not self.MDN:
            # check vel
            if -10 < self.VEL < 10:
                self.VEL = 10

            # update enc pos
            self.ENCPOS = self.ENCPOS + self.VEL * 0.1

            # check mel
            if self.ENCPOS <= self.MEL_LIM:
                self.ENCPOS = self.MEL_LIM
                self.CMDPOS = self.MEL_LIM
                self.MDN = True
                self.MEL = True
            else:
                self.MEL = False

            # check pel
            if self.ENCPOS >= self.PEL_LIM:
                self.ENCPOS = self.PEL_LIM
                self.CMDPOS = self.PEL_LIM
                self.MDN = True
                self.PEL = True
            else:
                self.PEL = False

            step = self.VEL * 0.1

            # check org
            if -step < self.ENCPOS - self.ORG_LIM <= step:
                self.ORG = True
                if self.ISCAPTUREHOME:
                    self.MDN = True
            else:
                self.ORG = False

            # check index
            if -step < self.ENCPOS - self.INDEX_LIM <= step:
                self.INDEX = True
                if self.ISCAPTUREINDEX:
                    self.MDN = True
            else:
                self.INDEX = False

            # check mdn
            if -step*1.5 < self.ENCPOS - self.CMDPOS < step*1.5:
                self.ENCPOS = self.CMDPOS
                self.MDN = True
                self.ISMOVE = False

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s' % (self.ENCPOS, self.CMDPOS, self.SERVO, self.ALARM, self.ASTP, self.MDN, self.PEL, self.MEL,self.ORG,self.INDEX)


if __name__ == '__main__':
    cd = CardDriver()
    print(cd.di)
    print(cd.do)
    print(cd.axis_status)
