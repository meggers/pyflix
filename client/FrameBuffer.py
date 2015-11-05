#!/usr/bin/python

import Queue

class FrameBuffer:

    def __init__(self, length):
        self.length = length
        self.last_frame_no = -1
        self.buffer = Queue.Queue(self.length)

    def add_frame(self, frame_number, frame):
        if not self.buffer.full() and self.last_frame_no == frame_number + 1:
            self.buffer.put((frame_number, frame))
            self.last_frame_no = frame_number
            return True
        else:
            return False

    def get_frame(self):
        if not self.buffer.empty():
            if self.buffer.qsize() == 1:
                self.last_frame_no = -1

            return self.buffer.get()
        else:
            return None

    def last_frame_added(self):
        return self.last_frame_no