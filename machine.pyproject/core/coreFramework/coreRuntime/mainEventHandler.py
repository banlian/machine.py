# -*- coding: utf-8 -*-

# !/usr/bin/env python3


from core.coreFramework.coreEvents.userEventHandler import UserEventHandler
from core.coreFramework.coreEvents.userEvent import UserEvent

import time


class MainEventHandler(UserEventHandler):

    def __init__(self, task):
        self.task = task
        self.state = 'wait'

        self._start_tick = 0
        self._is_finish = False

    def post_event(self, event_type):
        self.task.station.post_event(self, event_type)
        self.state = 'wait'
        self._is_finish = False

    def wait_event_done(self, timeout):
        if timeout < 0:
            while True:
                if self.task.setid > 0 and not self.task.is_running:
                    raise Exception('task cancelled')
                if self._is_finish:
                    return 0
                time.sleep(0.001)
        else:
            i = 0

            while True:

                if self.task.setid > 0 and not self.task.is_running:
                    raise Exception('task cancelled')
                if self._is_finish:
                    return 0

                if self.state == 'handling':
                    if i > timeout:
                        break
                    i += 1
                elif self.state == 'timeout':
                    # timeout branch
                    return -1

                time.sleep(0.001)

            return 0 if i <= timeout else -1

    def on_event_handle(self, event):
        return 0

    def on_event_handling(self):
        pass

    def on_signal(self, event):
        if self.state == 'handling':
            self.on_event_handling()
        elif self.state == 'done':
            self._is_finish = True
            self.state = 'wait'

    def on_alarm(self, event):
        pass

    def on_user_event(self, event):
        if self.state == 'wait' or self.state == 'handling':
            ret = self.on_event_handle(event)
            if ret == 0:
                self.state = 'handling'
                self._start_tick = time.time()

    def on_start(self, event):
        pass;

    def on_stop(self, event):
        self.state = 'stop'
        self._is_finish = False

    def on_reset(self, event):
        self.state = 'wait'
        self._is_finish = False

    def on_pause(self, event):
        if self.state == 'handling':
            self.state = 'pause'

    def on_continue(self, event):
        if self.state == 'pause':
            self.state = 'handling'
            # repeat handling
            self.on_user_event(event)
