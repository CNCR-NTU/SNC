import struct
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
id = b"0101"

cycles=1000
timestamp=0
model=1
timestepsize=0.05
model = 0
A= 1.0
B= 25.0
C = -1.0
D = 1.0
force = 0.0
stimuli = 0.0
esynmap1 = 0
esynmap2 = 0
weight=0.0

serialport='/dev/ttyUSB0'

if __name__ == "__main__":
    try:
        ser = serial.Serial(serialport, 115200)
        ser.flushInput()
        ser.flushOutput()
        serFlag=False
        time.sleep(0.1)
    except serial.serialutil.SerialException:
        print("The serial port is not available!")
        time.sleep(5)
        serFlag=False
    print("Muscle controller testbench. v0.1")
    print("Testing lmm for ", cycles, " cycles")
    #Reset
    op = b"0"
    command=reset+id+op
    command=struct.pack(">B",int(command,2))
    if serFlag==True:
        ser.write(command)
    print("Sending RESET: ",command)
    print("##########################################################")
    time.sleep(1)

    # Protected write
    op = b"1"
    command = write + id + op
    command = struct.pack(">B", int(command, 2))
    print("Sending protected write: ", command)
    timestampf = struct.pack(">Q", timestamp)
    timestepsize = struct.pack(">f", timestepsize)
    model = struct.pack(">H", 0)
    print("Sending timestamp: ", struct.unpack(">Q", timestampf)[0])
    print("Range: [63..0]")
    print("Sending time step size: ", struct.unpack(">f", timestepsize)[0])
    print("Range: [95..64]")
    print("Sending muscle selection: ", struct.unpack(">H", model)[0])
    print("Range: [111..64]")
    packet = command + model + timestepsize + timestampf
    print(packet, " ", len(packet) * 8 - 8)
    print("##########################################################")
    if serFlag == True:
        ser.write(timestampf)
        ser.write(packet)
        ser.write(model)
    time.sleep(0.1)

    # ++++++++++++++++++++++++++++++++++++++++++++++++
    # normal write
    op = b"0"
    command = write + id + op
    command = struct.pack(">B", int(command, 2))
    i=0
    #+A
    if serFlag==True:
        ser.write(command)
    print("Sending A command: ", command)
    lsb = i
    i+=32
    msb = lsb + 31
    print("Address [", msb, "..", lsb, "]")
    lsbc = struct.pack(">L", lsb)
    if serFlag == True:
        ser.write(lsbc)
    print("Sending LSB: ", lsbc)
    msbc = struct.pack(">L", msb)
    if serFlag == True:
        ser.write(msbc)
    print("Sending MSB: ", msbc)
    A=struct.pack(">f",A)
    if serFlag==True:
        ser.write(A)
    print("Sending A value: ", A)
    print("||||||||||||||||||||||||||||||||||||||||||")
    time.sleep(0.1)

    # +B
    if serFlag==True:
        ser.write(command)
    print("Sending B command: ", command)
    lsb = i
    i += 32
    msb = lsb + 31
    print("Address [", msb, "..", lsb, "]")
    lsbc = struct.pack(">L", lsb)
    if serFlag == True:
        ser.write(lsbc)
    print("Sending LSB: ", lsbc)
    msbc = struct.pack(">L", msb)
    if serFlag == True:
        ser.write(msbc)
    print("Sending MSB: ", msbc)
    B = struct.pack(">f", B)
    if serFlag==True:
        ser.write(B)
    print("Sending B value: ", B)
    print("||||||||||||||||||||||||||||||||||||||||||")
    time.sleep(0.1)

    # +C
    if serFlag==True:
        ser.write(command)
    print("Sending C command: ", command)
    lsb = i
    i += 32
    msb = lsb + 31
    print("Address [", msb, "..", lsb, "]")
    lsbc = struct.pack(">L", lsb)
    if serFlag == True:
        ser.write(lsbc)
    print("Sending LSB: ", lsbc)
    msbc = struct.pack(">L", msb)
    if serFlag == True:
        ser.write(msbc)
    print("Sending MSB: ", msbc)
    C = struct.pack(">f", C)
    if serFlag==True:
        ser.write(C)
    print("Sending C value: ", C)
    print("||||||||||||||||||||||||||||||||||||||||||")
    time.sleep(0.1)

    # +D
    if serFlag==True:
        ser.write(command)
    print("Sending D command: ", command)
    lsb = i
    i += 32
    msb = lsb + 31
    print("Address [", msb, "..", lsb, "]")
    lsbc = struct.pack(">L", lsb)
    if serFlag == True:
        ser.write(lsbc)
    print("Sending LSB: ", lsbc)
    msbc = struct.pack(">L", msb)
    if serFlag == True:
        ser.write(msbc)
    print("Sending MSB: ", msbc)
    D= struct.pack(">f", D)
    if serFlag==True:
        ser.write(D)
    print("Sending D value: ", D)
    print("||||||||||||||||||||||||||||||||||||||||||")
    time.sleep(0.1)

    # + force
    if serFlag==True:
        ser.write(command)
    print("Sending force value command: ", command)
    lsb = i
    i += 32
    msb = lsb + 31
    print("Address [", msb, "..", lsb, "]")
    lsbc = struct.pack(">L", lsb)
    if serFlag == True:
        ser.write(lsbc)
    print("Sending LSB: ", lsbc)
    msbc = struct.pack(">L", msb)
    if serFlag == True:
        ser.write(msbc)
    print("Sending MSB: ", msbc)
    force = struct.pack(">f", force)
    if serFlag==True:
        ser.write(force)
    print("Sending force value: ", force)
    print("||||||||||||||||||||||||||||||||||||||||||")
    time.sleep(0.1)

    # + stimulus
    if serFlag == True:
        ser.write(command)
    print("Sending stimulus command: ", command)
    lsb = i
    i += 32
    msb = lsb + 31
    print("Address [", msb, "..", lsb, "]")
    lsbc = struct.pack(">L", lsb)
    if serFlag == True:
        ser.write(lsbc)
    print("Sending LSB: ", lsbc)
    msbc = struct.pack(">L", msb)
    if serFlag == True:
        ser.write(msbc)
    print("Sending MSB: ", msbc)
    stimuli = struct.pack(">f", stimuli)
    if serFlag == True:
        ser.write(stimuli)
    print("Sending stimulus value: ", stimuli)
    print("||||||||||||||||||||||||||||||||||||||||||")
    time.sleep(0.1)

    # + esynmap1
    if serFlag == True:
        ser.write(command)
    print("Sending esynmap1 command: ", command)
    lsb = i
    i += 32
    msb = lsb + 31
    print("Address [", msb, "..", lsb, "]")
    lsbc = struct.pack(">L", lsb)
    if serFlag == True:
        ser.write(lsbc)
    print("Sending LSB: ", lsbc)
    msbc = struct.pack(">L", msb)
    if serFlag == True:
        ser.write(msbc)
    print("Sending MSB: ", msbc)
    esynmap1 = struct.pack(">L", esynmap1)
    if serFlag == True:
        ser.write(esynmap1)
    print("Sending esynmap1 value: ", esynmap1)
    print("||||||||||||||||||||||||||||||||||||||||||")
    time.sleep(0.1)

    # + esynmap2
    if serFlag == True:
        ser.write(command)
    print("Sending esynmap2 command: ", command)
    lsb = i
    i += 8
    msb = lsb + 7 # ++++++++++++++++++++++++++++++++++ size 8
    print("Address [", msb, "..", lsb, "]")
    lsbc = struct.pack(">L", lsb)
    if serFlag == True:
        ser.write(lsbc)
    print("Sending LSB: ", lsbc)
    msbc = struct.pack(">L", msb)
    if serFlag == True:
        ser.write(msbc)
    print("Sending MSB: ", msbc)
    esynmap2 = struct.pack(">L", esynmap2)
    if serFlag == True:
        ser.write(esynmap2)
    print("Sending esynmap2 value: ", esynmap2)
    print("||||||||||||||||||||||||||||||||||||||||||")
    time.sleep(0.1)

    j=0
    for I in range(0,20,1):
        if serFlag == True:
            ser.write(command)
        print("Sending weight",j,"command: ", command)
        lsb = i
        i += 32
        msb = lsb + 31
        print("Address [", msb, "..", lsb, "]")
        lsbc = struct.pack(">L", lsb)
        if serFlag == True:
            ser.write(lsbc)
        print("Sending LSB: ", lsbc)
        msbc = struct.pack(">L", msb)
        if serFlag == True:
            ser.write(msbc)
        print("Sending MSB: ", msbc)
        weightf = struct.pack(">f", weight)
        if serFlag == True:
            ser.write(weightf)
        print("Sending  weight",j,"value: ", weightf)
        j+=1
        print("||||||||||||||||||||||||||||||||||||||||||")
        time.sleep(0.1)
    print("##########################################################")
    # ++++++++++++++++++++++++++++++++++++++++++++++++
    # Restore state
    op = b"0"
    command = restoreState + id + op
    command = struct.pack(">B", int(command, 2))
    if serFlag==True:
        ser.write(command)
    print("Sending restore state: ", command)
    print("##########################################################")
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
        print("Timestamp: ", timestamp)
        # + stimulus
        op = b"0"
        command = write + id + op
        command = struct.pack(">B", int(command, 2))
        if serFlag == True:
            ser.write(command)
        print("Sending stimulus value: ", i, " , command: ", command)
        print("Address [", struct.unpack(">L",msbcStim)[0], "..", struct.unpack(">L",lsbcStim)[0], "]")
        if serFlag == True:
            ser.write(lsbcStim)
        #print("Sending LSB: ", lsbcStim)
        if serFlag == True:
            ser.write(msbcStim)
        #print("Sending MSB: ", msbcStim)
        if serFlag == True:
            ser.write(stimuli)
        print("Sending stimulus value: ", stimuli)
        print("||||||||||||||||||||||||||||||||||||||||||")
        #time.sleep(0.1)

        # runStep
        spikeTrain=0
        errorLog=0
        op = b"0"
        command = runStep + id + op
        command = struct.pack(">B", int(command, 2))
        if serFlag==True:
            ser.write(command)
        print("\n\nSending run step: ", command, ", timestamp: ", timestamp)
        for j in range (0,38,1):
            spikes=struct.pack(">B",0)
            #print("Sending spikes byte", j,"value:", spikes)
            if serFlag == True:
                ser.write(spikes)
        if serFlag == True:
            print("Reading results")
            s=ser.read(5)
            print("Results in raw: ", s)
            print("Length: ",len(s))
            print("Command: ",struct.unpack(">B",s[0:1])[0])
            res=struct.unpack(">f",s[1:5])[0]
            result.append(res)
    print("##########################################################")
    print(result)
    if serFlag==True:
        ser.close()



