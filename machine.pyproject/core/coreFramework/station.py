from core.coreFramework.coreEvents.userEventHandler import UserEventHandler, UserEventType
from core.coreFramework.coreRuntime.alarm import SystemAlarm


class Station(UserEventHandler):

    def __init__(self, setid, name, runtime):
        self.setid = setid
        self.name = name

        # station environment
        self.runtime = runtime
        self.stations = {}
        self.tasks = {}

        self.di = {}
        self.do = {}
        self.vio = {}
        self.axis = {}

        self.lights = {}
        self.signals = {'estop': [], 'door': [], 'safecurtain': [], 'automanual': [], 'start': [], 'stop': [], 'reset': []}

        # station states
        self.ct = 0
        self.state = 'auto'
        self.auto_state = 'waitreset'
        self.last_auto_state = 'waitreset'

    def __str__(self):
        return 'Station %s %s' % (self.name, self.setid)

    def __repr__(self):
        return self.__str__()


    # ---------------------------------- station events handling

    def handle_event(self, event):
        if self.setid == 0:
            # pass event to next level stations
            [s.handle_event(event) for s in self.stations.values() if s.setid > 0]
            # main task handle events
            [t.handle_event(event) for t in self.tasks.values() if t.setid == 0]
        else:
            # to make recursive station work
            # [s.handle_event(event) for s in self.stations if s.setid > 0]
            # pass station events to tasks
            [t.handle_event(event) for t in self.tasks.values() if t.setid > 0]
        super().handle_event(event)

    def on_signal(self, event):
        # check estop on
        if self.state != 'estop' and any([s.status for s in self.signals['estop']]):
            self.post_alarm(self, 'error', SystemAlarm.ESTOP, self.name)
            for s in self.stations.values():
                s.state = 'estop'
                s.auto_state = 'waitreset'

        # check estop off
        if self.state == 'estop':
            if all([not s.status for s in self.signals['estop']]):
                for s in self.stations.values():
                    s.state = 'error'
                    s.auto_state = 'waitreset'

        # check reset on error
        elif self.state == 'error':
            if all([not s.status for s in self.signals['reset']]):
                self.state = 'auto'
                self.auto_state = 'waitreset'
                for s in self.stations.values():
                    s.state = 'auto'
                    s.auto_state = 'waitreset'

        # check manual off
        elif self.state == 'manual':
            if any([not s.status for s in self.signals['automanual']]):
                self.state = 'auto'
                self.auto_state = 'waitreset'
                for s in self.stations.values():
                    if len(s.signals['automanual']) > 0:
                        s.state = 'auto'
                        s.auto_state = 'waitreset'

        elif self.state == 'auto':
            # check door
            if any([s.status for s in self.signals['door']]):
                # door activate
                self.last_auto_state = self.auto_state
                self.state = 'auto'
                self.auto_state = 'pause'
                for s in self.stations.values():
                    if len(s.signals['door']) > 0:
                        s.last_auto_state = s.auto_state
                        s.state = 'auto'
                        s.auto_state = 'pause'
                        s.post_alarm(s, 'warning', SystemAlarm.DOOR_OPEN, s.name)

            # check safe curtain
            if any([s.status for s in self.signals['safecurtain']]):
                # door activate
                self.last_auto_state = self.auto_state
                self.state = 'auto'
                self.auto_state = 'pause'
                for s in self.stations.values():
                    if len(s.signals['safecurtain']) > 0:
                        s.last_auto_state = s.auto_state
                        s.state = 'auto'
                        s.auto_state = 'pause'
                        s.post_alarm(s, 'warning', SystemAlarm.SAFECURTAIN_ACT, s.name)

            # check manual
            if any([s.status for s in self.signals['automanual']]):
                self.state = 'manual'
                self.auto_state = 'waitreset'
                for s in self.stations.values():
                    if len(s.signals['automanual']) > 0:
                        s.state = 'manual'
                        s.auto_state = 'waitreset'

            # check start/stop/reset
            if all([s.status for s in self.signals['start']]):
                for s in self.stations.values():
                    if len(s.signals['start']) > 0:
                        s.start()

            if all([s.status for s in self.signals['stop']]):
                for s in self.stations.values():
                    if len(s.signals['stop']) > 0:
                        s.pause()

            if all([s.status for s in self.signals['reset']]):
                for s in self.stations.values():
                    if len(s.signals['reset']) > 0:
                        s.reset()

        pass

    def on_alarm(self, event):
        pass

    def on_start(self, event):
        if self.state == 'auto':
            if self.auto_state == 'waitrun':
                self.auto_state = 'running'
            elif self.auto_state == 'pause':
                self.auto_state = self.last_auto_state
        pass

    def on_stop(self, event):
        if self.state == 'auto':
            if self.auto_state == 'running':
                self.auto_state = 'waitreset'
        pass

    def on_reset(self, event):
        if self.state == 'auto':
            if self.auto_state == 'waitreset':
                self.auto_state = 'resetting'
        pass

    def on_pause(self, event):
        if self.state == 'auto':
            if self.auto_state == 'running' or self.auto_state == 'resetting':
                self.last_auto_state = self.auto_state
                self.auto_state = 'pause'
        pass

    def on_continue(self, event):
        if self.state == 'auto':
            if self.auto_state == 'pause':
                if self.last_auto_state == 'running':
                    self.ct_start()
                self.auto_state = self.last_auto_state

        pass

    # ----------------------------------------

    # ---------------------------station start/stop/reset

    def start(self):
        if self.state == 'auto':
            if self.auto_state == 'waitrun':
                self.post_event(self, UserEventType.START)
            elif self.auto_state == 'pause':
                self.post_event(self, UserEventType.CONTINUE)
        pass

    def pause(self):
        if self.state == 'auto':
            if self.auto_state == 'running' or self.auto_state == 'resetting':
                self.post_event(self, UserEventType.PAUSE)
        pass

    def stop(self):
        if self.state == 'auto':
            if self.auto_state == 'running' \
                    or self.auto_state == 'resetting' \
                    or self.auto_state == 'waitrun' \
                    or self.auto_state == 'pause':
                self.post_event(self, UserEventType.STOP)
        pass

    def reset(self):
        if self.state == 'auto':
            if self.auto_state == 'waitreset':
                self.post_event(self, UserEventType.RESET)
        pass

    # ----------------------------

    # ----------------------ct methods
    def ct_start(self):
        pass

    def ct_stop(self):
        pass

    def ct_reset(self):
        pass

    # -----------------------------------

    # --------------------------------- post events methods

    def post_event(self, event_handler, event_type):
        self.runtime.post_event(event_handler, event_type)
        pass

    def post_alarm(self, station, alarm_level, alarm_id, alarm_msg):
        self.runtime.post_alarm(station, alarm_level, alarm_id, alarm_msg)
        pass

    def post_log(self, target, log_msg, log_level):
        self.runtime.post_log(target, log_msg, log_level)
        pass

    def post_data(self, target, data):
        self.runtime.post_data(target, data)
        pass

    # --------------------------------------------


if __name__ == '__main__':
    s = Station(2, 'test', None)
    print(str(s))
