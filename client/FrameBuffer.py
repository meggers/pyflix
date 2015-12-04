#!/usr/bin/python

import Queue

class FrameBuffer:

    def __init__(self, length):
        self.length = length
        self.buffer = Queue.PriorityQueue(length)

    def add_frame(self, frame_number, frame):
        try:
            self.buffer.put_nowait((frame_number, frame))
            return True
        except Queue.Full, e:
            # print "Full"
            return False

    def get_frame(self, frame_number):
        return_frame = self.peek()
        if return_frame != None and return_frame[0] != frame_number:
            print return_frame
            print frame_number
            print self.free_size()
            return None
        
        try:
            item = self.buffer.get_nowait()
            return item
        except Queue.Empty, e:
            # print "Empty"
            return None

    def free_size(self):
        return self.length - self.buffer.qsize()

    def ready(self):
        return self.buffer.qsize() >= (self.length / 2)
        
    def has(self, frame_number):
        return frame_number in self.num_buffer.queue
        
    def peek(self):
        try:
            return self.buffer.queue[0]
        except IndexError:
            return None
