#!/usr/bin/python

import Queue

class FrameBuffer:

    def __init__(self, length):
        self.length = length
        self.buffer = Queue.PriorityQueue(self.length)

    def add_frame(self, frame_number, frame):
        if not self.buffer.full():
            self.buffer.put((frame_number, frame))
            return True
        else:
            return False

    def get_frame(self):
        if not self.buffer.empty():
            return self.buffer.get()
        else:
            return None

    def ready(self):
        return self.buffer.qsize() >= (self.length / 4)
