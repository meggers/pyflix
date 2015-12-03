#!/usr/bin/python

from socket import *
from sys import *
import threading, time

class ServerManager():
    def __init__(self, servers, frame_buffer):
        self.current_frame = -1
        self.servers = servers
        self.frame_buffer = frame_buffer
        
    def start(self):
        port = 5005
        
        self.cons = [ServerConnection(ip, port, i * 8) for i, ip in enumerate(self.servers)]
        
        for ip, server in self.cons.iteritems():
            server.start()
        
        self.frame_queue.listen()
    
    def window_complete(self, id):
        print "COMPLETE: {}, t = {}".format(id, self.cons[id].delay)
        
        self.configs[id]['frm'] += self.configs[id]['wnd'] * self.configs[id]['del']
        
        if self.all_windows_done():
            self.reconfigure()
        
        if self.configs[id]['frm'] > 200:
            self.frame_queue.close()
        else:
            self.cons[id].start(self.configs[id])
            
            
    def all_windows_done(self):
        for id in xrange(0,4):
            if self.cons[id].receiving:
                return False
        return True
        
    def reconfigure(self):
        delays = [
            self.cons[0].delay,
            self.cons[1].delay,
            self.cons[2].delay,
            self.cons[3].delay
        ]
        
        
        
        
    def handle_frame(self, id, data):
        if len(data) == 0:
            self.window_complete(id)
        elif data == "ACK":
            print "Recvd ACK"
        else:
            frame_num = int(data[:5])
            print "Recvd frame: {}, length: {}".format(frame_num, len(data))
            
            
    # class FrameQueue():
    
    #     def __init__(self):
    #         self.q = Queue.Queue()
            
    #     def put(self, id, data):
    #         self.q.put((id, data))
            
    #     def get(self):
    #         return self.q.get()
            
    #     def close(self):
    #         self.done = True
            
    #     def listen(self):
    #         self.done = False
    #         while not self.done:
    #             id, data = self.get()
    #             servers.handle_frame(id, data)
                

        
class ServerConnection():
    
    def __init__(self, host, port, frame, window = 8):
        self.host = host
        self.port = port
        self.frame = frame
        self.window = window
        
        self.receiving = False
        self.delay = -1
        
    def tick(self):
        self.tick_time = time.time()
        
    def tock(self):
        return time.time() - self.tick_time
        
    def start(self):
        
        request = {"cmd": "Start", "frm": self.frame, "wnd": self.window}
        
        self.tick()
        self.receiving = True
        self.thread = threading.Thread(target=ServerConnection.threaded_send_request, args=(self, request)).start()
    
    def window_received(self):
        self.delay = self.tock()
        self.receiving = False
    
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
                
                servers.frame_queue.put(server.host, data + "")
                
        finally:
            sock.close()
            
        server.window_received()


    
    
    
    
    