#!/usr/bin/python

import Queue

class FrameBuffer:

    def __init__(self, length):
        self.length = length
        self.buffer = Queue.PriorityQueue(length)
        self.most_recent_watched = -1

    def add_frame(self, frame_number, frame):
        try:
            if not self.has((frame_number, frame)) and frame_number > self.most_recent_watched:
                self.buffer.put_nowait((frame_number, frame))
                # print "Add {}".format(frame_number)
                return True
            else:
                return False
        except Queue.Full as e:
            # print "Add Full"
            return False

    def get_frame(self, frame_number):
        return_frame = self.peek()
        if return_frame != None and return_frame[0] != frame_number:
            # print "Get {}, Next {}, Free {}".format(frame_number, return_frame[0], self.free_size())
            return None
        
        try:
            item = self.buffer.get_nowait()
            self.most_recent_watched = item[0]
            # print "Get OK {}".format(item[0])
            return item
        except Queue.Empty as e:
            # print "Get Empty"
            return None

    def free_size(self):
        return self.length - self.buffer.qsize()

    def ready(self):
        return self.buffer.qsize() >= (self.length / 2)
        
    def has(self, item):
        return item in self.buffer.queue
        
    def peek(self):
        try:
            return self.buffer.queue[0]
        except IndexError:
            return None
