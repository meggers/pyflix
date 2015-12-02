#!/usr/bin/python

from FrameBuffer import *
from MovieWatcher import *
from ConnectionHandler import *

# UDP static info
UDP_HOSTNAME = "0.0.0.0"
UDP_PORT = 5000

# server list
servers = [ "10.0.0.0" ]#"vm1" , "vm2", "vm3", "vm4"]

def main():
    global UDP_HOSTNAME, UDP_PORT, servers

    frame_buffer = FrameBuffer(32)

    movie_stream = ConnectionHandler(UDP_HOSTNAME, UDP_PORT, servers, frame_buffer)
    movie_stream.start()

    movie_thread = MovieWatcher(frame_buffer)
    movie_thread.start()

if __name__ == "__main__":
    main()