#!/usr/bin/python

import Queue

class FrameBuffer:

    def __init__(self, length):
        self.length = length
        self.buffer = Queue.Queue(self.length)

    def addFrame(self, frame_number, frame):
        self.buffer.put((frame_number, frame))

    def getFrame(self):
        return self.buffer.get()

