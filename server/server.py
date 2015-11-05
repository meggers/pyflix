import csv, json, SocketServer

class RequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        request_message = json.loads(self.request[0])
        socket = self.request[1]

        frame_no = int(request_message['frm'])

        print "Handling request for {0}".format(frame_no)
        response = {
            "frm": frame_no,
            "dta": self.server.movie_data[frame_no]
        }

        socket.sendto(json.dumps(response), self.client_address)

def seed_movie():

    movie_data = {}
    with open('movie_data.csv', 'rb') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            frame_no, frame_data = row[0], row[1]
            movie_data[int(frame_no)] = frame_data

    return movie_data

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 5000
    server = SocketServer.UDPServer((HOST, PORT), RequestHandler)

    print "Seeding movie data..."
    server.movie_data = seed_movie()

    print "Listening for requests..."
    server.serve_forever()