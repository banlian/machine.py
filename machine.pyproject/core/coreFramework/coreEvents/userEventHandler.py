# -*- coding: utf-8 -*-


'''
created on 2018-01-16

@author: zzz
'''

from core.coreFramework.coreEvents.userEvent import UserEventType


class UserEventHandler(object):

    def handle_event(self, event):
        if event.event_type == UserEventType.SIGNAL:
            self.on_signal(event)
        elif event.event_type == UserEventType.ALARM:
            self.on_alarm(event)
        elif event.event_type == UserEventType.START:
            self.on_start(event)
        elif event.event_type == UserEventType.STOP:
            self.on_stop(event)
        elif event.event_type == UserEventType.RESET:
            self.on_reset(event)
        elif event.event_type == UserEventType.PAUSE:
            self.on_pause(event)
        elif event.event_type == UserEventType.CONTINUE:
            self.on_continue(event)
        else:
            self.on_user_event(event)

    def on_signal(self, event):
        pass;

    def on_alarm(self, event):
        pass;

    def on_start(self, event):
        pass;

    def on_stop(self, event):
        pass;

    def on_reset(self, event):
        pass;

    def on_pause(self, event):
        pass;

    def on_continue(self, event):
        pass

    def on_user_event(self, event):
        pass