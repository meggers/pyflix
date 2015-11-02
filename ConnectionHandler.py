#!/usr/bin/python

import socket

class ConnectionHandler:

    FRAME_SIZE = 4096

    def __init__(self, hostname, port, servers, data_buffer):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((hostname, port))

        self.connections = []
        for ip in servers:
            self.connections.append(ServerConnection(sock, ip))

    # sends text over udp using global udp info
    def send_request(sock, message):
        sock.sendto(message, (address, 5000))

        for connection in self.connections:
            if self.connection.ready():

    # listens on udp port for any response
    def listen(sock):
        while True:
            data, addr = sock.recvfrom(FRAME_SIZE)
            if data:
                sock.close()
                return data