import socket 
import struct

#UDP_IP = "127.0.0.1"
#UDP_PORT = 5005
UDP_IP = "100.100.1.254"
UDP_PORT = 4000
MESSAGE = struct.pack(">B",253)
 
print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT)) 
