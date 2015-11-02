#!/usr/bin/python

import time, threading, FrameBuffer

# UDP static info
UDP_HOSTNAME = "0.0.0.0"
UDP_PORT = 5000

# server list
servers = ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4"]

def movie_watcher(frame_buffer):
  while True:
    try:
      frame_no, frame_data = frame_buffer.get_frame()
      print frame_no
      time.sleep(0.01)
    except Queue.Empty:
      time.sleep(0.001)
      pass

def main(argv):
    global UDP_HOSTNAME, UDP_PORT

    frame_buffer = FrameBuffer(32)

    watcher = threading.Thread(target=movie_watcher, args=(frame_buffer,))

if __name__ == "__main__":
   main()