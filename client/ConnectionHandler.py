#!/usr/bin/python

from socket import *
from sys import *
import threading, time, Queue

class ServerManager():
    def __init__(self, servers, frame_buffer):
        self.highest_frame_requested = -1
        self.servers = servers
        self.frame_buffer = frame_buffer
        self.complete_queue = ServerManager.CompleteQueue()
        
    def start(self):
        port = 5005
        
        self.cons = [ServerConnection(self, ip, port, i * 8) for i, ip in enumerate(self.servers)]
        self.highest_frame_requested = (4 * 8) - 1
        
        for server in self.cons:
            server.start()
        
        self.complete_queue.listen(self)
    
    def window_complete(self, id):
        print "COMPLETE: {}, t = {}".format(id, self.cons[id].delay)
        
        if self.cons[id].frame < 29999:
            # TODO Modify stuff here
            self.cons[id].frame = self.highest_frame_requested + total_fleight_size()
            self.cons[id].window = 8
            self.highest_frame_requested += self.cons[id].frame + self.cons[id].window
            self.cons[id].start()
            
        elif total_fleight_size() == 0:
            self.complete_queue.close()
            
    def total_fleight_size():
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
        
        self.fleight_size = 0
        self.receiving = False
        self.delay = -1
        
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
        self.manager.complete_queue.put(self.ip)
    
    @staticmethod
    def threaded_send_request(server, request):
        
        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket(AF_INET, SOCK_STREAM)
        # Connect to server
        sock.connect((server.host, server.port))
        
        # Send data
        sock.sendall(json.dumps(request)+"\n")
        try:
            done = False
            while not done:
                # Receive data from the server
                data = sock.recv(1030)
                
                if len(data) == 0:
                    done = True
                else:
                    server.fleight_size -= 1
                
                frame_num = int(data[:5])
                if server.manager.frame_queue.add_frame(frame_num, data) and server.frame < frame_num:
                    server.frame = frame_num
                
        finally:
            sock.close()
            
        server.request_complete()
