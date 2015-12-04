#!/usr/bin/python

import time, threading

class MovieWatcher(threading.Thread):
    
    def __init__ (self, frame_buffer):
        self.current_frame = 0
        self.frame_buffer = frame_buffer
        threading.Thread.__init__ (self)
    
    def run(self):
        # wait until queue is buffered
        while True:
            if self.frame_buffer.ready():
                break
            else:
                time.sleep(.01)

        # watch movie
        while True:
            frame = self.frame_buffer.get_frame(self.current_frame)
            if frame is not None:
                self.current_frame += 1
                if frame[0] % 1 == 0:
                    print frame[0]
                time.sleep(0.01)
            else:
                time.sleep(0.0001)