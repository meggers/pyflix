import json, SocketServer

class RequestHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        while 1:
            if self.command == "Start":
                response = self.server.movie_data[start_frame]
                self.wfile.write(response)

            self.rfile.readline().strip()
            request_message = json.loads(self.rfile.readline().strip())

            self.command = request_message['cmd']
            self.parameter = int(request_message['prm'])
            self.start_frame = int(request_message['frm'])



def seed_movie():
    movie_data = {}
    with open('movie_data.txt', 'rb') as f:
        lines = f.readlines()
        for line in lines:
            clean_line = line.rstrip()
            frame_no = int(line[:5])
            movie_data[frame_no] = line

    return movie_data

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 5000
    server = SocketServer.TCPServer((HOST, PORT), RequestHandler)

    print "Seeding movie data..."
    server.movie_data = seed_movie()

    print "Listening for requests..."
    server.serve_forever()