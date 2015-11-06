#!/usr/bin/python

import json, threading, SocketServer, os, struct

class DataHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        response_message = self.request[0]
        socket = self.request[1]

        print response_message
        print type(response_message)
        print os.getsizeof(response_message)
        frame_no = struct.unpack("I", frame_bin[0:3])[0]

        if self.server.data_buffer.add_frame(frame_no, response_message):
            request_frame = frame_no + 4
        else:
            request_frame = frame_no

        request = {"frm": request_frame}

        socket.sendto(json.dumps(request), self.client_address)

class ConnectionHandler(threading.Thread):

    def __init__(self, hostname, port, server_ips, data_buffer):
        self.port = port
        self.server_ips = server_ips
        self.server = SocketServer.UDPServer((hostname, port), DataHandler)
        self.server.data_buffer = data_buffer
        threading.Thread.__init__ (self)

    def run(self):
        print "Starting movie stream..."
        for index, ip in enumerate(self.server_ips):
            self.server.socket.sendto(json.dumps({"frm": index}), (ip, self.port))

        print "Listening on port..."
        self.server.serve_forever()