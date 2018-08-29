from core.coreDriver.gtsCard import Gts800Card
from core.coreDriver.virtualCard import VIOCard, VirtualAxisCard

from core.coreFramework.coreRuntimeDriver.driver import *
from core.coreFramework.coreRuntimeDriver.axis import *
from core.coreFramework.coreRuntimeDriver.gpio import *

from core.coreFramework.coreRuntime.alarmEventHandler import SystemAlarm

from core.coreFramework.stationRuntime import StationRuntime, Station, StationTask, Runtime
from machinedemo.station1.task1 import Task1,Task2

import sys,time

class Loading(object):

    def __init__(self):
        self.runtime = None
        self.vcarddrv = None
        self.viodrv = None

    def build_runtime(self):

        Runtime.RUNTIME_LOG_LEVEL = 'debug'

        self.runtime = StationRuntime()

        # driver initialize
        self.vcarddrv = AxisDriver(VirtualAxisCard(), 1, 'virtualdriver')
        self.viodrv = AxisDriver(VIOCard(), 2, 'viodriver')

        self.vcarddrv.initialize()
        self.viodrv.initialize()

        self.runtime.driver = {1: self.vcarddrv, 2: self.viodrv}

        # di/do/vio/axis initialize
        for i in range(32):
            self.runtime.di[i] = Di(self.vcarddrv, i, 'Di%s' % i)
            self.runtime.do[i] = Do(self.vcarddrv, i, 'Do%s' % i)
            self.runtime.vio[i] = Vio(self.viodrv, i, 'Vio%s' % i)

        self.runtime.axis[1] = Axis(self.vcarddrv, 1, 0, 'axis1', 1, 100, 100, None)
        self.runtime.axis[2] = Axis(self.vcarddrv, 2, 1, 'axis2', 1, 100, 100, None)

        # stations
        self.runtime.stations[1] = Station(1, 'station1', self.runtime)

        # tasks
        self.runtime.tasks[1] = Task1(1, 'task1', self.runtime.stations[1])
        self.runtime.tasks[2] = Task2(2, 'task2', self.runtime.stations[1])
        self.runtime.tasks[1].set_station(self.runtime.stations[1])

        # station task relation build
        self.runtime.stations[1].tasks[1] = self.runtime.tasks[1]
        #self.runtime.stations[1].tasks[2] = self.runtime.tasks[2]

        self.runtime.stations[1].axis[1] = self.runtime.axis[1]

        # station signals

    def initialize(self):
        ret = [drv.initialize() for drv in self.runtime.driver.values()]
        if any(ret):
            self.runtime.main.error(SystemAlarm.DRIVER_INIT_FAIL, ','.join([drv.name for drv in self.runtime.driver.values()]))

        self.runtime.initialize()
        pass

    def terminate(self):
        self.runtime.terminate()

    def join(self):
        [t.join() for t in self.runtime.tasks.values()]


if __name__ == '__main__':

    l = Loading()
    l.build_runtime()
    print(str(l.runtime))

    print('build runtime finish...')

    l.initialize()
    print('initialize runtime')

    l.runtime.stations[1].reset()

    l.join()
    time.sleep(5)

    print('main finish...')