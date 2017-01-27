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


# a=0.02, b=0.2, c=-65, d=6,v_th=30mv, V=-70mv, U=-14.0mv
v_th = 30.0
a=0.02
b = 0.2
c = -65.0
d = 6.0
V=-70.0
U=-14.0
esynmap1 = 0
esynmap2 = 0
weight=0.0
stimuli = 7.0

serialport='/dev/ttyUSB0'
#IZK neuron model
if __name__ == "__main__":
    try:
        ser = serial.Serial(serialport, 115200)
        ser.flushInput()
        ser.flushOutput()
        serFlag=True
        #time.sleep(0.1)
    except serial.serialutil.SerialException:
        print("The serial port is not available!")
        #time.sleep(5)
        serFlag=False
    cycles=1000
    timestamp=0
    model=0
    timestepsize=0.5
    print("IZK controller testbench. v0.1")
    print("Testing muscle model 1 for ", cycles, " cycles")
    #Reset
    op = b"0"
    command=reset+id+op
    command=struct.pack(">B",int(command,2))
    if serFlag==True:
        ser.write(command)
    print("Sending RESET: ",command)
    print("##########################################################")
    #time.sleep(1)

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
    print("Range: [111..96]")
    packet = command + model + timestepsize + timestampf
    print(packet, " ", len(packet)*8-8)
    print("##########################################################")
    if serFlag == True:
        ser.write(packet)
    #time.sleep(0.1)
    
    # ++++++++++++++++++++++++++++++++++++++++++++++++
    # standard write
    op = b"0"
    command = write + id + op
    command = struct.pack(">B", int(command, 2))

    # v_th=30mv
    i=0
    if serFlag == True:
        ser.write(command)
    print("Sending v_th command: ", command)
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
    v_th = struct.pack(">f", v_th)
    if serFlag == True:
        ser.write(v_th)
    print("Sending v_th: ", v_th)
    print("||||||||||||||||||||||||||||||||||||||||||")
    #time.sleep(0.1)

    # a=0.02
    if serFlag==True:
        ser.write(command)
    print("Sending A command: ", command)
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
    a=struct.pack(">f",a)
    if serFlag==True:
        ser.write(a)
    print("Sending A value: ", a)
    print("||||||||||||||||||||||||||||||||||||||||||")
    #time.sleep(0.1)

    # b=0.2
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
    b = struct.pack(">f", b)
    if serFlag==True:
        ser.write(b)
    print("Sending B value: ", b)
    print("||||||||||||||||||||||||||||||||||||||||||")
    #time.sleep(0.1)

    #c=-65
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
    c = struct.pack(">f", c)
    if serFlag==True:
        ser.write(c)
    print("Sending C value: ", c)
    print("||||||||||||||||||||||||||||||||||||||||||")
    #time.sleep(0.1)

    #d=6
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
    d = struct.pack(">f", d)
    if serFlag==True:
        ser.write(d)
    print("Sending D value: ", d)
    print("||||||||||||||||||||||||||||||||||||||||||")
    #time.sleep(0.1)

    if serFlag==True:
        ser.write(command)
    print("Sending V command: ", command)
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
    V = struct.pack(">f", V)
    if serFlag==True:
        ser.write(V)
    print("Sending V value: ", V)
    print("||||||||||||||||||||||||||||||||||||||||||")
    #time.sleep(0.1)

    if serFlag==True:
        ser.write(command)
    print("Sending U command: ", command)
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
    U = struct.pack(">f", U)
    if serFlag==True:
        ser.write(U)
    print("Sending U value: ", U)
    print("||||||||||||||||||||||||||||||||||||||||||")
    #time.sleep(0.1)

    # + stimulus
    if serFlag == True:
        ser.write(command)
    print("Sending stimulus command: ", command)
    lsb = i
    i += 32
    msb = lsb + 31
    print("Address [", msb, "..", lsb, "]")
    lsbcStim = struct.pack(">L", lsb)
    if serFlag == True:
        ser.write(lsbcStim)
    print("Sending LSB: ", lsbcStim)
    msbcStim = struct.pack(">L", msb)
    if serFlag == True:
        ser.write(msbcStim)
    print("Sending MSB: ", msbcStim)
    stimuli = struct.pack(">f", stimuli)
    if serFlag == True:
        ser.write(stimuli)
    print("Sending stimulus value: ", stimuli)
    print("||||||||||||||||||||||||||||||||||||||||||")
    #time.sleep(0.1)

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
    #time.sleep(0.1)

    # + esynmap2
    if serFlag == True:
        ser.write(command)
    print("Sending esynmap2 command: ", command)
    lsb = i
    i += 8
    msb = lsb + 7  # ++++++++++++++++++++++++++++++++++ size 8
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
    #time.sleep(0.1)

    j = 0
    for I in range(0, 20, 1):
        # + stimulus
        if serFlag == True:
            ser.write(command)
        print("Sending stimulus value: ", i, " , command: ", command)
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
        if serFlag == True:
            ser.write(stimuli)
        print("Sending stimulus value: ", stimuli)
        print("||||||||||||||||||||||||||||||||||||||||||")
        #time.sleep(0.1)

        if serFlag == True:
            ser.write(command)
        print("Sending weight", j, "command: ", command)
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
        print("Sending  weight", j, "value: ", weightf)
        j += 1
        print("||||||||||||||||||||||||||||||||||||||||||")
        #time.sleep(0.1)

    # ++++++++++++++++++++++++++++++++++++++++++++++++
    # Restore state
    op = b"0"
    command = restoreState + id + op
    command = struct.pack(">B", int(command, 2))
    if serFlag==True:
        ser.write(command)
    print("Sending restore state: ", command)
    print("##########################################################")
    #time.sleep(0.1)
    ser.flushInput()
    # ++++++++++++++++++++++++++++++++++++++++++++++++

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
            s=ser.read(1)
            print("Results in raw: ", s)
            print("Length: ",len(s))
            res=struct.unpack(">B",s[0:1])[0]
            if res==98:
                spk=False
            elif res==99:
                spk=True
                spikeTrain+=1
            else:
                spk="Error"
                errorLog+=1
            result.append(spk)
    print("##########################################################")
    print(result)
    print("Spikes:",spikeTrain)
    print("Errors:", errorLog)
    if serFlag==True:
        ser.close()
