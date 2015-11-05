#!/usr/bin/python

import json, threading, SocketServer

class DataHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        response_message = json.loads(self.request[0])
        socket = self.request[1]

        frame_no = int(response_message['frm'])

        if self.server.data_buffer.add_frame(frame_no, response_message['dta']):
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