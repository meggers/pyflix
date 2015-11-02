import threading
import time

class MovieWatcher(threading.Thread):
    
    def __init__ (self, frame_buffer):
        self.frame_buffer = frame_buffer
        self.empty_count = 0
        threading.Thread.__init__ (self)
    
    def run(self):
        while True:
            if self.empty_count >= 5000:
                print "No frames received in the five seconds. Exiting Movie Watcher."
                break

            frame = self.frame_buffer.get_frame()
            if frame is not None:
                print frame
                self.empty_count = 0;
                time.sleep(0.01)
            else:
                self.empty_count += 1
                time.sleep(0.001)
