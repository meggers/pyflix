import json, SocketServer

# class RequestHandler(SocketServer.BaseRequestHandler):
class RequestHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        
        while 1:
            try
                self.data = self.request.recv(1024)
            except:
                break

            if not self.data:
                break
                
            self.data = self.data.strip()
            request_message = json.loads( self.data.strip() )

            self.command = request_message['cmd']
            self.window = int(request_message['wnd'])
            self.start_frame = int(request_message['frm'])

            if self.command == "Start":

                for offset in range(self.window):
                    response = self.server.movie_data[self.start_frame + offset]
                    self.request.send(response)

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
    HOST, PORT = "0.0.0.0", 5005
    server = SocketServer.TCPServer((HOST, PORT), RequestHandler)

    print "Seeding movie data..."
    server.movie_data = seed_movie()

    print "Listening for requests..."
    server.serve_forever()