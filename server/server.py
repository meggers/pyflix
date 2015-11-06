import json, SocketServer

class RequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        request_message = json.loads(self.request[0])
        socket = self.request[1]

        frame_no = int(request_message['frm'])

        print "Handling request for {0}".format(frame_no)

        response = self.server.movie_data[frame_no]
        socket.sendto(json.dumps(response), self.client_address)

def seed_movie():
    movie_data = {}
    with open('movie_data.txt', 'rb') as f:
        lines = f.readlines()
        for line in lines:
            frame_no = int(line[:5])
            move_data[frame_no] = line

    return movie_data

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 5000
    server = SocketServer.UDPServer((HOST, PORT), RequestHandler)

    print "Seeding movie data..."
    server.movie_data = seed_movie()

    print "Listening for requests..."
    server.serve_forever()