#!/usr/bin/python

import threading, time

class MovieWatcher(threading.Thread):
    
    def __init__ (self, frame_buffer):
        self.frame_buffer = frame_buffer
        self.empty_count = 0
        threading.Thread.__init__ (self)
    
    def run(self):
        start = time.time()
        last_time = 0
        while True:
            if self.empty_count >= 50000:
                print "No frames received in the five seconds. Exiting Movie Watcher."
                break

            frame = self.frame_buffer.get_frame()
            if frame is not None:
                self.empty_count = 0
            else:
                self.empty_count += 1
                time.sleep(0.0001)
