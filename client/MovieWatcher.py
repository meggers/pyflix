#!/usr/bin/python

import threading, time

class MovieWatcher(threading.Thread):
    
    def __init__ (self, frame_buffer):
        self.frame_buffer = frame_buffer
        self.empty_count = 0
        threading.Thread.__init__ (self)
    
    def run(self):
        while True:
            frame = self.frame_buffer.get_frame()
            if frame is not None:
                if frame[0] % 100 == 0:
                    print frame[0] 