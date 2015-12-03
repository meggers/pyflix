#!/usr/bin/python

import time, threading

class MovieWatcher(threading.Thread):
    
    def __init__ (self, frame_buffer):
        self.frame_buffer = frame_buffer
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
                print frame[0]
                time.sleep(0.01)
            else:
                time.sleep(0.0001)