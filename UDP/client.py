import socket 
import struct
import time

UDP_IP = "100.100.1.255"
UDP_PORT = 4000
#reset
#msg = b'\x00\x00\xff\xfc\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


#msg+= struct.pack(">H",1) #dest id
#msg+= struct.pack(">H",65533) #source id
#msg+= struct.pack(">B",14) # command
#msg+= struct.pack(">Q",0) # timestamp
#msg+= struct.pack(">L",25) #payload size
#msg+= struct.pack(">L",4) # time step size
#msg+= struct.pack(">Q", 1000) # number of cycles
#msg+= struct.pack(">Q", 1) # simulation id
#msg+= struct.pack(">H", 2) # timeout period
#msg+= struct.pack(">H", 3) # number of neurons
#msg+= struct.pack(">B", 4) # number of muscles
#print(len(msg))
 
#print("UDP target IP:", UDP_IP)
#print("UDP target port:", UDP_PORT)
#print("message:", msg)
 
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#sock.sendto(msg, (UDP_IP, UDP_PORT)) 

#time.sleep(1)
#Send run step
msg=b'\x00\x00\xff\xff\r\x00\x00\x00\x00\x00\x00=\xa2\x00\x00\x00&\x99=\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
print(len(msg))
 
print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", msg)
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.sendto(msg, (UDP_IP, UDP_PORT)) 
