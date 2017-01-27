import socket
import sys
import struct
import time
import numpy as np

HOST, PORT = "100.100.0.1", 3000
#data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    #Configure simulation
    msg=b'\x00\x01\xff\xfc\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x00\x00\xc3P\x00\x01\x01\x10\x08\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x00@\xa0\x00\x00\x00\x02\x01\x10\x08\x00\x00\x00 \x00\x00\x00?\x00\x00\x00\x00\x00\x00\x00\x00BH\x00\x00\x00\x03\x01\x10\x08\x00\x00\x00@\x00\x00\x00_\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x04\x02\x10\x08\x00\x00\x00`\x00\x00\x00\x7f\x00\x00\x00\x00\x00\x00\x00\x1f@\x00\x00\x00\x00\x05\x01\x10\x08\x00\x00\x00\x80\x00\x00\x00\x9f\x00\x00\x00\x00\x00\x00\x00\x00D4\x00\x00\x00\x06\x01\x10\x08\x00\x00\x00\xa0\x00\x00\x00\xbf\x00\x00\x00\x00\x00\x00\x00\x00=\xb8Q\xec\x00\x07\x01\x10\x08\x00\x00\x00\xc0\x00\x00\x00\xdf\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x01\x10\x08\x00\x00\x00\xe0\x00\x00\x00\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\t\x01\x10\x08\x00\x00\x01\x00\x00\x00\x01\x1f\x00\x00\x00\x00\x00\x00\x00\x00=\xb8Q\xec\x00\n\x01\x10\x08\x00\x00\x01 \x00\x00\x01?\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    print(len(msg))
    sock.sendall(msg)

    # Receive data from the server and shut down
    received = int(struct.unpack('>B',sock.recv(1))[0])
    if received==200:
        print("The packet was transmited with success!")
    else:
        print("Error. The packet was not transmited!")
    print("Sent:     {}".format(msg))
finally:
    sock.close()
    
time.sleep(1)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    # PCS
    msg=b'\x00\x01\xff\xfc\x13\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x00\x00\x00\x00\x00\x00\x00\x01\xff\xf3\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00'
    
    print(len(msg))
    sock.sendall(msg)

    # Receive data from the server and shut down
    received = int(struct.unpack('>B',sock.recv(1))[0])
    if received==200:
        print("The packet was transmited with success!")
    else:
        print("Error. The packet was not transmited!")
    print("Sent:     {}".format(msg))
finally:
    sock.close()

time.sleep(1)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    # Define network topology
    msg=b'\x00\x01\xff\xfc\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00&\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06'
    print(len(msg))
    sock.sendall(msg)

    # Receive data from the server and shut down
    received = int(struct.unpack('>B',sock.recv(1))[0])
    if received==200:
        print("The packet was transmited with success!")
    else:
        print("Error. The packet was not transmited!")
    print("Sent:     {}".format(msg))
finally:
    sock.close()

time.sleep(1)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    # New timestamp
    msg=b'\x00\x01\xff\xfc\x0d\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x26'
    for i in range(0,38,1):
        msg+=struct.pack(">B",np.random.randint(0,255))
    print(len(msg))
    sock.sendall(msg)

    # Receive data from the server and shut down
    received = int(struct.unpack('>B',sock.recv(1))[0])
    if received==200:
        print("The packet was transmited with success!")
    else:
        print("Error. The packet was not transmited!")
    print("Sent:     {}".format(msg))
finally:
    sock.close()






