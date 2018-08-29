# -*- coding: utf-8 -*-


'''
created on 2018-01-16

@author: zzz
'''

from queue import PriorityQueue  # 优先队列
from core.coreFramework.coreEvents.userEvent import UserEventType
import time


class EventServer(object):

    def __init__(self, name):
        self.Name = name
        self._queue = PriorityQueue()

    def empty(self):
        return self._queue.empty()

    def post(self, event, priority=0):
        self._queue.put((priority, event))

    def dispatch(self):
        while self._queue.qsize() > 0:
            q = self._queue.get()
            q[1].execute()
            if q[1].event_type != UserEventType.SIGNAL:
                print(q[1])
            del q


class TestEvent(object):

    def __init__(self, event_type, event_name):
        self.time = time.time()
        self.event_type = event_type
        self.event_name = event_name

    def execute(self):
        print('%s %s\r\n' % (self.event_type, self.event_name))

    def __lt__(self, other):
        return self.time < other.time


if __name__ == '__main__':
    es = EventServer("test")

    es.post(TestEvent('p0', 'test01'), 0)
    es.post(TestEvent('p0', 'test02'), 0)
    es.post(TestEvent('p1', 'test11'), 1)
    es.post(TestEvent('p1', 'test12'), 1)
    es.post(TestEvent('p2', 'test21'), 2)
    es.post(TestEvent('p2', 'test22'), 2)

    es.dispatch()
