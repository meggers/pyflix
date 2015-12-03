import json, SocketServer

class RequestHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        request_message = json.loads( self.rfile.readline().rstrip() )

        self.command = request_message['cmd']
        self.window = int(request_message['prm'])
        self.start_frame = int(request_message['frm'])

        if self.command == "Start":

            for offset in range(window):
                response = self.server.movie_data[start_frame + offset]
                self.wfile.write(response)

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