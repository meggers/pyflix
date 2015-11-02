import csv, json, SocketServer

class RequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        request_message = json.loads(self.request[0])
        socket = self.request[1]

        frame_no = request_message['frm']
        response = {
            "frm": frame_no,
            "dta": self.server.movie_data[frame_no]
        }

        socket.sendto(response, self.client_address)

def seed_movie():

    movie_data = {}
    with open('movie_data.csv', 'rb') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            frame_no, frame_data = row[0], row[1]
            movie_data[frame_no] = frame_data

    return movie_data

if __name__ == "__main__":
    HOST, PORT = "localhost", 5000
    server = SocketServer.UDPServer((HOST, PORT), RequestHandler)
    server.movie_data = seed_movie()
    server.serve_forever()