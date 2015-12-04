#!/usr/bin/python

import Queue, ThreadedFrameQueue

class FrameBuffer:

    def __init__(self, length):
        self.length = length
        # self.buffer = Queue.PriorityQueue(length)
        self.buffer = ThreadedFrameQueue.ThreadedFrameQueue(length)
        # self.most_recent_watched = -1

    def add_frame(self, frame_number, frame):
        
        try:
            self.buffer.put(frame_number, frame)
            return True
        except ThreadedFrameQueue.Full as e:
            return False
        except ThreadedFrameQueue.Seen as e:
            return True
        except ThreadedFrameQueue.Duplicate as e:
            return True
        
        
        
        # try:
        #     if self.has((frame_number, frame)):
        #         print "Duplicate Add"
        #         return True
        #     if frame_number > self.most_recent_watched:
        #         self.buffer.put_nowait((frame_number, frame))
        #         return True
        #     else:
        #         print "Add too low"
        #         return True
        # except Queue.Full as e:
        #     # print "Add Full"
        #     return False

    def get_frame(self, frame_number):
        
        return self.buffer.get(frame_number)
        
        
        # return_frame = self.peek()
        # if return_frame != None and return_frame[0] != frame_number:
        #     # print "Get {}, Next {}, Free {}".format(frame_number, return_frame[0], self.free_size())
        #     return None
        
        # try:
        #     item = self.buffer.get_nowait()
        #     self.most_recent_watched = frame_number
        #     # print "Get OK {}".format(item[0])
        #     return item
        # except Queue.Empty as e:
        #     # print "Get Empty"
        #     return None

    def free_size(self):
        return self.buffer.free_size()
        return self.length - self.buffer.qsize()

    def ready(self):
        return self.buffer.qsize() >= (self.length / 2)
        
    # def has(self, item):
    #     return item in self.buffer.queue
        
    # def peek(self):
    #     try:
    #         return self.buffer.queue[0]
    #     except IndexError:
    #         return None
