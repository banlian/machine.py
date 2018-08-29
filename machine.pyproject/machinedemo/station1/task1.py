from core.coreFramework.stationTask import StationTask

import time

class Task1(StationTask):

    def reset_loop(self):
        print('task1 reset loop start...')

        # set vio
        print(','.join([str(v.status) for v in self.station.runtime.vio.values()]))
        print(self.station.runtime.vio[1].status)
        print('setvio')
        self.setvio([1], [1])
        print(self.station.runtime.vio[1].status)
        print(','.join([str(v.status) for v in self.station.runtime.vio.values()]))

        # set do
        print(','.join([str(v.status) for v in self.station.runtime.do.values()]))
        print(self.station.runtime.do[1].status)
        print('setdo')
        self.setdo([1, 3, 5], [1, 1, 1])
        print(self.station.runtime.do[1].status)
        print(','.join([str(v.status) for v in self.station.runtime.do.values()]))

        print('homestatus:' + str(self.station.runtime.axis[1].home))
        self.movehome([1], -1)
        print('homestatus:' + str(self.station.runtime.axis[1].home))

        self.is_running = False

    def run_loop(self):
        print('task run loop start...')

        print(','.join([str(v.status) for v in self.station.runtime.vio.values()]))
        print(self.station.runtime.vio[1].status)
        print('setvio')
        self.setvio(1, 1)
        print(self.station.runtime.vio[1].status)
        print(','.join([str(v.status) for v in self.station.runtime.vio.values()]))

        self.is_running = False


class Task2(StationTask):

    def reset_loop(self):
        while self.is_running:
            a = self.station.runtime.axis[1]
            print('%s %s pos:%s enc:%s cmd:%s homestate:%s mdn:%s org:%s' % (a.name, a.setid, a.curpos, a.encpos, a.cmdpos, a.home_state, a.mdn, a.org))
            time.sleep(0.1)


if __name__ == '__main__':
    print('main')
    t = Task1(1,"task1", None)
    t.start()
