#!/usr/bin/python

from socket import *
from sys import *
import threading, time, Queue, json

class ServerManager():
    def __init__(self, servers, frame_buffer):
        self.highest_frame_requested = -1
        self.servers = servers
        self.frame_queue = frame_buffer
        self.complete_queue = ServerManager.CompleteQueue()
        
    def start(self):
        port = 5005
        
        self.cons = [ServerConnection(self, ip, port, i * 8) for i, ip in enumerate(self.servers)]
        self.highest_frame_requested = (4 * 8) - 1
        
        for server in self.cons:
            server.start()
        
        self.complete_queue.listen(self)

    def generate_window(self, connection):
        flight_sizes = [ x.flight_sizes for x in self.cons ]
        total_fleight_size = sum(flight_sizes) 
        buffer_space = self.frame_buffer.free_size()
        request_amt = buffer_space - total_fleight_size

        if request_amt <= 0:
            # if we have requested as much as we have room for already
            # just ask for a little bit, a frame will probably be read!
            return 1
        elif request_amt <= connection.window:
            # if we need less than we asked for last time
            return request_amt
        else:
            # grab delays per packet for each connection and inverse weight proportion
            delays = [ x.delay / x.window for x in self.cons ]
            weight = sum(delays)/(connection.delay + sum(delays))

            # calculate window size as percentage of free space
            window = int(weight * request_amt)

            # return window if window is greater than 1, else 1
            # this is to ensure we still have delay data for connection
            return max(1, window)
    
    def window_complete(self, id):
        server_index = 0
        for index, server in enumerate(self.cons):
            if server.host == id:
                server_index = index
        
        # print "COMPLETE: "+id+", t = {}".format(self.cons[server_index].delay)
        
        if self.cons[server_index].frame < 29999:
            self.cons[server_index].frame = self.highest_frame_requested
            self.cons[server_index].window = self.generate_window(self.cons[server_index])
            self.highest_frame_requested = self.cons[server_index].frame + self.cons[server_index].window

            self.cons[server_index].start()
        elif self.total_fleight_size() == 0:
            self.complete_queue.close()
            
    def total_fleight_size(self):
        fs = 0
        for server in self.cons:
            fs += server.fleight_size
        return fs
       
    class CompleteQueue():
    
        def __init__(self):
            self.q = Queue.Queue()
            
        def put(self, id):
            self.q.put(id)
            
        def get(self):
            return self.q.get()
            
        def close(self):
            self.done = True
            
        def listen(self, handler):
            self.done = False
            while not self.done:
                id = self.get()
                handler.window_complete(id)
        
class ServerConnection():
    
    def __init__(self, manager, host, port, frame, window = 8):
        self.manager = manager
        self.host = host
        self.port = port
        self.frame = frame
        self.window = window
        
        self.frame_size = 2048
        self.fleight_size = 0
        self.receiving = False
        self.delay = -1
        self.starting_frame = frame
        
        # Create a socket (SOCK_STREAM means a TCP socket)
        self.sock = socket(AF_INET, SOCK_STREAM)
        # Connect to server
        self.sock.connect((self.host, self.port))
        
    def tick(self):
        self.tick_time = time.time()
        
    def tock(self):
        return time.time() - self.tick_time
        
    def start(self):
        request = {"cmd": "Start", "frm": self.frame, "wnd": self.window}
        
        self.tick()
        self.fleight_size = self.window
        self.receiving = True
        self.thread = threading.Thread(target=ServerConnection.threaded_send_request, args=(self, request)).start()
    
    def request_complete(self):
        self.delay = self.tock()
        self.receiving = False
        self.fleight_size = 0
        
        if self.starting_frame + self.window - 1 > self.frame:
            self.window -= self.frame - self.starting_frame
            self.fleight_size = self.window
            self.starting_frame = self.frame
            self.start()
        else:
            self.manager.complete_queue.put(self.host)
    
    @staticmethod
    def threaded_send_request(server, request):
        
        num_recvd = 0
        
        # Send data
        server.sock.sendall(json.dumps(request)+"\n")
        # sock.sendto(json.dumps(request)+"\n", (server.host, server.port))
        try:
            done = False
            data = ""
            frames = ""
            server.starting_frame = server.frame
            while not done:
                # Receive data from the server
                server.frame_size = 1018
                data += server.sock.recv(server.frame_size)
                # if the frame_size == 2048 then its the first frame, adjust this to fit the following frame
                if server.frame_size == 2048:
                    server.frame_size = len(data)
                    
                # print "frame {}".format(data)
                
                if len(data) >= server.frame_size:
                    
                    server.fleight_size -= 1
                    num_recvd += 1
                    frame_num = int(data[:5])
                    frame = data[:server.frame_size]
                    data = data[server.frame_size:]
                    # print "frame: {}".format(frame_num)
                    
                    was_added = server.manager.frame_queue.add_frame(frame_num, frame)
                    if was_added:
                        if server.frame < frame_num:
                            server.frame = frame_num
                    else:
                        pass
                        # server.fleight_size = 0
                        # done = True
                        
                if server.fleight_size == 0:
                    done = True
                    
        finally:
            pass
            
        server.request_complete()
