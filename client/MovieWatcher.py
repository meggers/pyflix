#!/usr/bin/python

import sys, time, threading

class MovieWatcher(threading.Thread):
    
    def __init__ (self, frame_buffer):
        self.frame_buffer = frame_buffer
        self.empty_count = 0
        threading.Thread.__init__ (self)
    
    def run(self):
        # wait until queue is buffered
        while True:
            if self.frame_buffer.ready():
                break
            else:
                time.sleep(.5)

        # watch movie
        while True:
            frame = self.frame_buffer.get_frame()
            if frame is not None:
                if frame[0] % 100 == 0:
                    print frame[0] 