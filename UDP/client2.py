import socket 
import struct

UDP_IP = "192.168.0.7"
UDP_PORT = 4000
MESSAGE = struct.pack(">B",255)
 
print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT)) 
