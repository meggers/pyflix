#!/usr/bin/python

import sys, getopt, json

# UDP static info
UDP_HOSTNAME = "0.0.0.0"
UDP_PORT = 5000

# server list
servers = ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4"]

# message size

def main(argv):
    global UDP_HOSTNAME, UDP_PORT

    # parse our command line arguments
    try:
      opts, args = getopt.getopt(argv, "u:m:s:", ["username=","moviename=","starttime="])
    except getopt.GetoptError:
      print 'client.py -u <username> -m <moviename> -s <starttime>'
      sys.exit(2)
    for opt, arg in opts:
        if opt in ("-u", "--username"):
            username = arg
        elif opt in ("-m", "--moviename"):
            moviename = arg
        elif opt in ("-s", "--starttime"):
            starttime = arg

if __name__ == "__main__":
   main(sys.argv[1:])