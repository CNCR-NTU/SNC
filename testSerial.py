import serial
import struct

ser = serial.Serial('/dev/ttyS4',115200)

print(ser.name)
for I in range(0,511,1):
    if I<256:
        tmp=I
    else:
        tmp=510-I
    ser.write(struct.pack(">B",tmp))
    s=ser.read(1)
    print(struct.unpack(">B",s)[0])
ser.close()
