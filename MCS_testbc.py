import  struct
import time
import serial

# Define commands
reset=b"000"
restoreState=b"001"
runStep=b"010"
sendSpike=b"011"
mapSBInput=b"100"
confNetTop=b"101"
write=b"110"
read=b"111"

#Define IDs
id = b"0001"

serialport='/dev/ttyUSB0'

if __name__ == "__main__":
    try:
        ser = serial.Serial(serialport, 115200)
        ser.flushInput()
        ser.flushOutput()
        serFlag=True
        time.sleep(0.1)
    except serial.serialutil.SerialException:
        print("The serial port is not available!")
        time.sleep(5)
        serFlag=False
    cycles=1000
    timestamp=0
    model=0
    timestepsize=0.05
    print("Muscle controller testbench. v0.1")
    print("Testing muscle model 1 for ", cycles, " cycles")
    #Reset
    op = b"0"
    command=reset+id+op
    command=struct.pack(">B",int(command,2))
    if serFlag==True:
        ser.write(command)
    print("Send RESET: ",command)
    time.sleep(1)

    # Protected write
    op = b"1"
    command = write + id + op
    command = struct.pack(">B", int(command, 2))

    print("Send protected write: ", command)
    timestepsize = struct.pack(">f", timestepsize)
    print("Sending time step size: ", struct.unpack(">f", timestepsize)[0])
    model = 1
    model=struct.pack(">B", model)
    packet=command+timestepsize+model
    print(packet," ",len(packet))
    if serFlag==True:
        ser.write(packet)
    print("Send muscle selection: ", struct.unpack(">B",model)[0])
    time.sleep(0.1)

    # ++++++++++++++++++++++++++++++++++++++++++++++++
    # normal write
    op = b"0"
    command = write + id + op
    command = struct.pack(">B", int(command, 2))
    i=0
    if serFlag == True:
        ser.write(command)
    print("Send weight: ", i + 1, " , command: ", command)
    lsb = i * 32
    msb = lsb + 31
    print("Address [", msb, "..", lsb, "]")
    lsbc = struct.pack(">L", lsb)
    if serFlag == True:
        ser.write(lsbc)
    print("Send LSB: ", lsbc)
    msbc = struct.pack(">L", msb)
    if serFlag == True:
        ser.write(msbc)
    print("Send MSB: ", msbc)
    weight = 1.0
    weight = struct.pack(">f", weight)
    if serFlag == True:
        ser.write(weight)
    print("Send weight: ", weight)
    time.sleep(0.1)


    if serFlag==True:
        ser.write(command)
    print("Send theta 3: ", i, " , command: ", command)
    i+=1
    lsb = i * 32
    msb = lsb + 31
    print("Address [", msb, "..", lsb, "]")
    lsbc = struct.pack(">L", lsb)
    if serFlag == True:
        ser.write(lsbc)
    print("Send LSB: ", lsbc)
    msbc = struct.pack(">L", msb)
    if serFlag == True:
        ser.write(msbc)
    print("Send MSB: ", msbc)
    theta3=3.0
    theta3=struct.pack(">f",theta3)
    if serFlag==True:
        ser.write(theta3)
    print("Send theta 3 value: ", theta3)
    time.sleep(0.1)

    if serFlag==True:
        ser.write(command)
    print("Send theta 0: ", i, " , command: ", command)
    i += 1
    lsb = i * 32
    msb = lsb + 31
    print("Address [", msb, "..", lsb, "]")
    lsbc = struct.pack(">L", lsb)
    if serFlag == True:
        ser.write(lsbc)
    print("Send LSB: ", lsbc)
    msbc = struct.pack(">L", msb)
    if serFlag == True:
        ser.write(msbc)
    print("Send MSB: ", msbc)
    theta0 = 5.0
    theta0 = struct.pack(">f", theta0)
    if serFlag==True:
        ser.write(theta0)
    print("Send theta 0 value: ", theta0)
    time.sleep(0.1)

    if serFlag==True:
        ser.write(command)
    print("Send theta 1: ", i, " , command: ", command)
    i += 1
    lsb = i * 32
    msb = lsb + 31
    print("Address [", msb, "..", lsb, "]")
    lsbc = struct.pack(">L", lsb)
    if serFlag == True:
        ser.write(lsbc)
    print("Send LSB: ", lsbc)
    msbc = struct.pack(">L", msb)
    if serFlag == True:
        ser.write(msbc)
    print("Send MSB: ", msbc)
    theta1 = -0.033333333333
    theta1 = struct.pack(">f", theta1)
    if serFlag==True:
        ser.write(theta1)
    print("Send theta 1 value: ", theta1)
    time.sleep(0.1)

    if serFlag==True:
        ser.write(command)
    print("Send theta 2: ", i, " , command: ", command)
    i += 1
    lsb = i * 32
    msb = lsb + 31
    print("Address [", msb, "..", lsb, "]")
    lsbc = struct.pack(">L", lsb)
    if serFlag == True:
        ser.write(lsbc)
    print("Send LSB: ", lsbc)
    msbc = struct.pack(">L", msb)
    if serFlag == True:
        ser.write(msbc)
    print("Send MSB: ", msbc)
    theta2 = 0.8333333333333
    theta2 = struct.pack(">f", theta2)
    if serFlag==True:
        ser.write(theta2)
    print("Send theta 2 value: ", theta2)
    time.sleep(0.1)

    if serFlag==True:
        ser.write(command)
    print("Send force: ", i, " , command: ", command)
    i += 1
    lsb = i * 32
    msb = lsb + 31
    print("Address [", msb, "..", lsb, "]")
    lsbc = struct.pack(">L", lsb)
    if serFlag == True:
        ser.write(lsbc)
    print("Send LSB: ", lsbc)
    msbc = struct.pack(">L", msb)
    if serFlag == True:
        ser.write(msbc)
    print("Send MSB: ", msbc)
    force = 0.0
    force = struct.pack(">f", force)
    if serFlag==True:
        ser.write(force)
    print("Send force value: ", force)
    time.sleep(0.1)

    # ++++++++++++++++++++++++++++++++++++++++++++++++
    # Restore state
    op = b"0"
    command = restoreState + id + op
    command = struct.pack(">B", int(command, 2))
    if serFlag==True:
        ser.write(command)
    print("Send restore state: ", command)
    time.sleep(0.1)
    ser.flushInput()
    # ++++++++++++++++++++++++++++++++++++++++++++++++
    #Run Step
    op = b"0"
    command = runStep + id + op
    command = struct.pack(">B", int(command, 2))
    if serFlag==True:
        ser.flushInput()
        ser.flushOutput()
    result=[]
    for j in range(0,200,1):
        timestamp+=1
        if serFlag==True:
            ser.write(command)
        print("\n\nSend run step: ", command, ", timestamp: ", timestamp)
        weight = 50.0
        weight = struct.pack(">f", weight)
        if serFlag == True:
            ser.write(weight)
        print("Sending weight: ", weight)
        print("Timestamp: ", timestamp)
        if serFlag == True:
            print("Reading results")
            s=ser.read(5)
            print("Results in raw: ", s)
            print("Length: ",len(s))
            print("Command: ",struct.unpack(">B",s[0:1])[0])
            res=struct.unpack(">f",s[1:5])[0]
            result.append(res)
    print(result)
    if serFlag==True:
        ser.close()



