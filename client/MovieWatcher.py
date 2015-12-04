#!/usr/bin/python

import time
import threading

class MovieWatcher(threading.Thread):
        

    def __init__ (self, frame_buffer, movie_length):
        self.last_time = self.current_milli_time()
        self.current_frame = 0
        self.frame_buffer = frame_buffer
        self.movie_length = movie_length
        self.times = []
        threading.Thread.__init__ (self)
        
    # current_milli_time = staticmethod(lambda: int(round(time.time() * 1000)))
    def current_milli_time(self):
        return int(round(time.time() * 1000))
    
    def run(self):
        global time
        
        # wait until queue is buffered
        while True:
            if self.frame_buffer.ready():
                break
            else:
                time.sleep(0.01)

        # watch movie
        while self.current_frame < self.movie_length:
            frame = self.frame_buffer.get_frame(self.current_frame)
            self.current_frame += 1
            temp_time = self.current_milli_time()
            self.times.append(temp_time - self.last_time)
            self.last_time = temp_time
            print frame[0]
            time.sleep(0.01)

        print "Dumping data..."
        target = open('data_dump.csv', 'w')
        target.truncate()
        for index, time in enumerate(self.times):
            target.write("{},{}".format(index, time / 10))

        target.close()