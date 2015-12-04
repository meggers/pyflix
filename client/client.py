#!/usr/bin/python

from FrameBuffer import *
from MovieWatcher import *
from ConnectionHandler import *

def main():
    servers = ["vm1" , "vm2", "vm3", "vm4"]

    frame_buffer = FrameBuffer(32)

    movie_thread = MovieWatcher(frame_buffer)
    movie_thread.start()

    movie_stream = ServerManager(servers, frame_buffer)
    movie_stream.start()

if __name__ == "__main__":
    main()