from http.server import BaseHTTPRequestHandler
import os
import requests
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
import socket
import socketserver
import time
import threadsDef as td
import struct
from subprocess import Popen, PIPE
import shlex

    
class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(bytes("<html><head><title>Model controller</title></head>", "utf-8"))
        self.wfile.write(bytes("<body><p>Model controller version: %s</p>" % str(td.MCversion), "utf-8"))
        self.wfile.write(bytes("<p>Ethernet Blaster. Only accepts sof files. </p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

        
    def do_POST(self):
        """ Handle POST Request"""
        # Check if path is there.
        if self.path:
            # Get length of the data and read it.
            length = self.headers['content-length']
            if int(length) > 30000000:
                if self.path[len(self.path) - 3:len(self.path)] == "sof":
                    data = self.rfile.read(int(length))
                    # Write the data to a file in current dir.
                    with open("/home/pedro/Ethernet_Blaster/" + self.path, 'wb+') as file:
                        file.write(data)
                    string = "File " + self.path[10:len(self.path)] + " was accepted! at " + time.strftime(
                        "%d/%m/%Y %H:%M:%S") + "\n"
                    print(string)
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    log = "The file was received with success!\nThe process to program the FPGA has started and it will take about 1 minute to complete!\n"
                    print(log)
                    path = "P;" + "/home/pedro/Ethernet_Blaster" + self.path
                    path += "@1"
                    par1 = "/home/pedro/altera/16.0/qprogrammer/bin/quartus_pgm"
                    par2 = "-z"
                    par3 = "--mode=JTAG"
                    par4 = "-o"
                    par5 = path
                    cmd = par1 + " " + par2 + " " + par3 + " " + par4 + " " + par5
                    process = Popen(shlex.split(cmd), stdout=PIPE)
                    (output, err) = process.communicate()
                    self.wfile.write(output)
                    exit_code = process.wait()
                    log = "Deleting file " + self.path[10:len(self.path)] + "!\n"
                    print(log)
                    os.remove("/home/pedro/Ethernet_Blaster/" + self.path)
                    log = "File deleted.\n"
                    print(log)
                    if exit_code == 0:
                        log = "The FPGA was configured with success!\n"
                    else:
                        log = "ERROR! The FPGA was NOT configured!\n"
                    exit_code = "Exit code: " + str(exit_code) + "\n"
                    err = "External code error: " + str(err) + "\n"
                    self.wfile.write(log.encode())
                    self.wfile.write(err.encode())
                    self.wfile.write(exit_code.encode())
                    print(exit_code)
                    print(err)
                    print(log)
                else:
                    log = "ERROR: File size error!\nThe FPGA was NOT configured!\nExit code: -1\n"
                    self.wfile.write(log.encode())
                    print(log)
            else:
                err=-2
                exit_code=0
                log = "ERROR: Empty packet!\nThe FPGA was NOT configured!\nExit code: -2\n"
                self.wfile.write(log.encode())
                self.wfile.write(err.encode())
                self.wfile.write(exit_code.encode())
                print(log)

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        data = self.request.recv(100024).strip()
        td.qi.put([data])
        log = "[MC dm - " + time.strftime("%d/%m/%Y %H:%M:%S") + "] TCP packet has been processed!"
        print(log)
        print(data)
        # just send back the same data, but upper-cased
        aux=struct.pack('>B',200)
        print(log, " code: 200")
        self.request.sendall(aux)


class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        td.qi.put([data])
        log = "[MC dm - " + time.strftime("%d/%m/%Y %H:%M:%S") + "] UDP packet has been processed!"
        print(log)
        print(data)

def TCPclient(packet):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST, PORT = "100.100.1.110", 3000
    print("Sending packet: ", packet, " to ", HOST, ":",PORT)
    try:
        sock.connect((HOST, PORT))
        sock.sendall(packet)
        received = int(struct.unpack('>B', sock.recv(1))[0])
        if received == 200:
            print("The packet was transmited with success!")
        else:
            print("Error. The packet was not transmited!")
    finally:
        sock.close()

