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
        start_window = 8
        
        self.cons = [ServerConnection(self, ip, port, i * start_window) for i, ip in enumerate(self.servers)]
        self.highest_frame_requested = (len(self.servers) * start_window) - 1
        
        for server in self.cons:
            server.start()
        
        self.complete_queue.listen(self)

    def generate_window(self, connection):
        # maximum possible window size if delay of connection is approaching 0
        # relative to other delays
        max_window = 125

        # delays of each connection per frame
        delays = [ x.delay / x.window for x in self.cons ]

        # weight of this connections delay in comparison with total delay
        # if each delay is one this evaluates to:
        # weight = 4/(1 + 4) = 4/5
        weight = float(sum(delays))/float(float(connection.delay/connection.window) + sum(delays))

        # window as a function of the maximum window and the weight of this connection
        # when all delays are equal this evaluates to:
        # 4/5 * 125 = 100 
        window = int(weight * max_window)

        # floor windows at 1 to avoid closing connections ?
        return max(1, window)
    
    def window_complete(self, id):
        server_index = 0
        for index, server in enumerate(self.cons):
            if server.host == id:
                server_index = index
        
        if self.cons[server_index].frame < 29999:
            self.cons[server_index].frame = self.highest_frame_requested + 1
            self.cons[server_index].window = self.generate_window(self.cons[server_index])
            self.highest_frame_requested += self.cons[server_index].window

            self.cons[server_index].start()
        elif self.total_flight_size() == 0:
            self.complete_queue.close()
            
    def total_flight_size(self):
        return sum([ server.flight_size for server in self.cons ])
       
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

    current_milli_time = staticmethod(lambda: int(round(time.time() * 1000)))
    
    def __init__(self, manager, host, port, frame, window = 8):
        self.manager = manager
        self.host = host
        self.port = port
        self.frame = frame
        self.window = window
        
        self.frame_size = 1024
        self.flight_size = 0
        self.receiving = False
        self.delay = 1500 # in ms
        self.starting_frame = frame
        
        # Create a socket (SOCK_STREAM means a TCP socket)
        self.sock = socket(AF_INET, SOCK_STREAM)
        # Connect to server
        self.sock.connect((self.host, self.port))
        
    def tick(self):
        self.tick_time = self.current_milli_time()
        
    def tock(self):
        return self.current_milli_time() - self.tick_time
        
    def start(self):
        request = {"cmd": "Start", "frm": self.frame, "wnd": self.window}
        
        self.tick()
        self.flight_size = self.window
        self.receiving = True
        self.thread = threading.Thread(target=ServerConnection.threaded_send_request, args=(self, request)).start()
    
    def request_complete(self):
        self.delay = self.tock()
        self.receiving = False
        
        self.flight_size = 0
        self.manager.complete_queue.put(self.host)
    
    @staticmethod
    def threaded_send_request(server, request):
        
        num_recvd = 0
        
        # Send request
        server.sock.sendall(json.dumps(request)+"\n")
        
        try:
            done = False
            data = ""
            frames = ""
            server.starting_frame = server.frame
            num_frames_needed = server.flight_size
            while not done:
                # Receive data from the server
                data += server.sock.recv(server.frame_size)
                
                if len(data) >= server.frame_size:
                    
                    frame_num = int(data[:5])
                    frame = data[:server.frame_size]
                    data = data[server.frame_size:]
                    
                    if server.manager.frame_queue.add_frame(frame_num, frame):
                        if server.frame < frame_num:
                            server.frame = frame_num
                        
                    num_frames_needed -= 1
                        
                # If we've gotten all of the frames for this window
                if num_frames_needed == 0:
                    done = True
                    
        finally:
            pass
            
        server.request_complete()
