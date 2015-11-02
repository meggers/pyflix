#!/usr/bin/python

from FrameBuffer import *
from MovieWatcher import *

# UDP static info
UDP_HOSTNAME = "0.0.0.0"
UDP_PORT = 5000

# server list
servers = ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4"]

def main():
  global UDP_HOSTNAME, UDP_PORT

  frame_buffer = FrameBuffer(32)

  movie_thread = MovieWatcher(frame_buffer)
  movie_thread.start()

if __name__ == "__main__":
   main()