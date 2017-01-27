import socketserver
import struct
import socket

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(102400).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        print (len(self.data))
        # just send back the same data, but upper-cased
        aux=struct.pack('>B',200)
        self.request.sendall(aux)

if __name__ == "__main__":
    HOST, PORT = "", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    print(s.getsockname()[0])
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
