#!/usr/bin/python

import Queue

class FrameBuffer:

    def __init__(self, length):
        self.length = length
        self.buffer = Queue.PriorityQueue(self.length)

    def add_frame(self, frame_number, frame):
        
        try:
            self.buffer.put_nowait((frame_number, frame))
            return True
        except Queue.Full, e:
            return False

    def get_frame(self):
        if not self.buffer.empty():
            return self.buffer.get()
        else:
            return None

    def free_size(self):
        return self.length - self.buffer.qsize()

    def ready(self):
        return self.buffer.qsize() >= (self.length / 2)
