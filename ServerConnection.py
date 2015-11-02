#!/usr/bin/python

class ServerConnection:

    def __init__(self, sock, ip):
        self.sock = sock
        self.ip = ip