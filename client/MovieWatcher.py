#!/usr/bin/python

import time, threading

class MovieWatcher(threading.Thread):
    
    def __init__ (self, frame_buffer, movie_length):
        self.current_frame = 0
        self.frame_buffer = frame_buffer
        self.movie_length = movie_length
        threading.Thread.__init__ (self)
    
    def run(self):
        # wait until queue is buffered
        while True:
            if self.frame_buffer.ready():
                break
            else:
                time.sleep(.01)

        # watch movie
        while self.current_frame < self.movie_length:
            frame = self.frame_buffer.get_frame(self.current_frame)
            self.current_frame += 1
            print frame[0]
            time.sleep(0.01)