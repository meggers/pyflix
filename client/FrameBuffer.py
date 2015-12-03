#!/usr/bin/python

import Queue

class FrameBuffer:

    def __init__(self, length):
        self.length = length
        self.buffer = Queue.PriorityQueue(length)
        self.num_buffer = Queue.PriorityQueue(length)

    def add_frame(self, frame_number, frame):
        try:
            if not self.num_buffer.empty() and self.num_buffer.queue[0] + self.length < frame_number:
                return False
            
            self.buffer.put_nowait((frame_number, frame))
            self.num_buffer.put_nowait(frame_number)
            # print "add {}".format(frame_number)
            return True
        except Queue.Full, e:
            # print "Full"
            return False

    def get_frame(self, frame_number):
        
        if not self.has(frame_number):
            # print "Not found"
            return None
        
        try:
            item = self.buffer.get_nowait()
            self.num_buffer.get_nowait()
            return item
        except Queue.Empty, e:
            # print "Empty"
            return None
        
        # if not self.buffer.empty():
        #     return self.buffer.get()
        # else:
        #     return None

    def free_size(self):
        return self.length - self.buffer.qsize()

    def ready(self):
        return True
        return self.buffer.qsize() >= (self.length / 2)
        
    def has(self, frame_number):
        return frame_number in self.num_buffer.queue
        
