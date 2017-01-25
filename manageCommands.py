# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 12:03:02 2016

@author: pedromachado
"""
from collections import deque
import threadsDef as td
import downloadManager as dm
import lxml.etree as ET # this library is necesssary to parse xml files
import time
import binascii
import struct

'''||||||||||||||||||||| Simulation commands ||||||||||||||||||||||||||||||||'''
#List of commands
cStart = struct.pack(">B",0)                      #x00 Start a new simulation
cLoadSDCP = struct.pack(">B",1)                   #x01 Load SDCP
cStop = struct.pack(">B",2)                      #x02 Stop current simulation
cQuery = struct.pack(">B", 3)                      #x03 Query
cRTWResults = struct.pack(">B",4)                 #x04 RTW results
cAbort = struct.pack(">B",5)                    #x05 Abort
''' TO DO '''
cErrorDetect = struct.pack(">B",6)                #x06 Error detected

cListSDCP = struct.pack(">B",7)                  #x07 List of SDCP

""" TO DO """
cNeuronMuscleID = struct.pack(">B",8)             #x08 Neuron or Muscle ID

cSynInStates = struct.pack(">B",9)                #x09 List of synaptic input states
cNonSpkRes = struct.pack(">B",10)                 #x0A Non-spiking neuron results
cConfigNetTop = struct.pack(">B",11)              #x0B Config Network Topology
cMusclesColRes = struct.pack(">B",12)             #x0C Muscles Collated Results
cNewTmStp = struct.pack(">B",13)                  #x0D new Time Step
cConfSim = struct.pack(">B",14)                   #x0E Configure Simulation
cReset = struct.pack(">B",15)                     #x0F reset the FPGA
cRTW = struct.pack(">B",16)                       #x10 Define RTW

""" TO DO: Check """
cFileUp = struct.pack(">B",17)                    #x11 File uploaded

cIMVer = struct.pack(">B",18)                     #x12 IM version
cPreconfStim = struct.pack(">B",19)               #x13 Preconfigured stimuli
cIniMuscleIt = struct.pack(">B",20)               #x14 Initialise muscle items

""" TO DO """
cCreateSDCP = struct.pack(">B",21)                #x15 create new SDCP

cSpkRes = struct.pack(">B",22)                    #x16 spiking neuron results
cMuscleRes = struct.pack(">B",23)                 #x17 Muscle Results
cInitNeuron = struct.pack(">B",24)                #x18 Initialise neuron items

""" TO DO """
cACK = struct.pack(">B",25)                       #x19 Acknowledge

cRuntimeStim = struct.pack(">B",26)               #x1A Runtime stimulus

"""TO DO: Check"""
cNMCVer = struct.pack(">B",27)                    #x1B Neuron/Muscle Controller version

cSimStateRes = struct.pack(">B",28)               #x1C Simulation State result
cDefineItemVal = struct.pack(">B",29)             #x1D Define item value
cListVar = struct.pack(">B",30)                   #x1E List of variables
cSimID = struct.pack(">B",31)                     #x1F Simulation ID

""" TO DO: Implement """
cListStimTp = struct.pack(">B",32)                #x20 List of Stimulus types

""" TO DO: Implement """
cMapSBinput = struct.pack(">B",33)                 #x21 Sensitivity Table

""" TO DO: Implement """
cXML2HexVer = struct.pack(">B",34)                #x22 XML2HexApp version

## -------------Queries -------------------------------------------------------------
""" TO DO """
numQueries = struct.pack(">B",10)
qListSDCP = struct.pack(">B",1)                  #x01 List SDCP
qListVar = struct.pack(">B",2)                    #x02 List Variables
qLtSimInStatus = struct.pack(">B",3)              #x03 List Simulation Input States
qChSimStatus = struct.pack(">B",4)               #x04 Check Simulation Status
qChNMCVer = struct.pack(">B",5)                  #x05 Check Neuron Controller Version
qChNeuronID = struct.pack(">B",6)                 #x06 Check Neuron Controller ID
qChSimID = struct.pack(">B",7)                    #x07 Check Simulation ID
qListStimSt = struct.pack(">B",8)                 #x08 List Stimuli states
qXML2HexVer = struct.pack(">B",9)                 #x09 XML2HexApp version
qIMVer = struct.pack(">B",10)                     #x0A IM version

## -------------Acknowledges ---------------------------------------------------------
""" TO DO """
aFileUp = struct.pack(">B",1)                     #x01 File uploaded
aDataConv = struct.pack(">B",2)                   #x02 Data conversion
aSimStatus = struct.pack(">B",3)                  #x03 Simulation Status
aRunStimSyncEnd = struct.pack(">B",4)             #x04 Runtime Stimulus Synchronisation End
#----------------------parameters for variable payload
IMserver=struct.pack(">H",65534)
IMFPGA=struct.pack(">H",65535)
SC=struct.pack(">H",65532)
PE=struct.pack(">H",65533)
RUS=struct.pack(">H",65531)
DMDServer=struct.pack(">H",65530)

# Model controller controls
# Define commands
mcReset=b"000"
mcRestoreState=b"001"
mcRunStep=b"010"
mcSendSpike=b"011"
mcMapSBInput=b"100"
mcConfNetTop=b"101"
mcWrite=b"110"
mcRead=b"111"

#Define IDs
mcIds = [b"0001",b"0010",b"0011",b"0100",b"0101"]
mcBid = b"0000"


def getEthAddress(dest,queueEthAddr):

    if dest>0 and dest<256:
        IP="100.100.0."
        IP+=str(dest)
        port=5000
        print("Packet to be sent to neuron : ", dest, " IP: ", IP, " Port: ", port)
        queueEthAddr.append(IP)
        queueEthAddr.append(port)
        errorFlag=False
        errorDest=False
    elif dest>255 and dest<303:
        IP="10.42.1."
        IP+=str(dest-255)
        port=5000
        print("Packet to be sent to neuron : " , dest, " IP: ", IP, " Port: ", port)
        queueEthAddr.append(IP)
        queueEthAddr.append(port)
        errorFlag=False
        errorDest=False
    elif dest>302 and dest<438:
        IP="10.42.1."
        IP+=str(int(float((dest-302)/5)+47.8))
        port=5000
        print("Packet to be sent to muscle : ", dest-302, " IP: ", IP, " Port: ", port)
        queueEthAddr.append(IP)
        queueEthAddr.append(port)
        errorFlag=False
        errorDest=False
    elif dest==0:
        IP="10.42.1.255"
        port=5000
        print("Packet to be sent to all neurons and muscles.", " IP: ", IP, " Port: ", port)
        queueEthAddr.append(IP)
        queueEthAddr.append(port)
        errorFlag=False
        errorDest=False
    elif dest>=IMserver:
        print("File to be processed by the IM.")
        errorFlag=True
        errorDest=False
    elif dest==XML2HexApp:
        print("File to be processed by the XML2HexApp.")
        errorFlag=True
        errorDest=False
    elif dest==RUS:
        endpoint="http://x.x.x.x:xxxx/RUS_endpoint"
        print("File to be sent to ", endpoint)
        queueEthAddr.append(endpoint)
        errorFlag=False
        errorDest=False
    elif dest==PE:
        endpoint="http://192.168.1.2:1735/PEIF/api/input"
        print("File to be sent to ", endpoint)
        queueEthAddr.append(endpoint)
        errorFlag=False
        errorDest=False
    elif dest==SC:
        endpoint=("http://172.16.1.2:1730/SC/api/emulator/im")
        print("File to be sent to ", endpoint)
        queueEthAddr.append(endpoint)
        errorFlag=False
        errorDest=False
    else:
        print("Error: Wrong destination ID!")
        errorFlag=True
        errorDest=True
    return queueEthAddr, errorFlag, errorDest




"""
procedure deleteAllsimulationData() - Delete all files

"""        

def deleteAllsimulationData(): #To be implemented
    log="[IM mc - " + time.strftime("%d/%m/%Y %H:%M:%S")+"] TO DO Deleting all simulation data!"
    file=open("IM.log","a+")
    file.write("\n"+log)
    file.close()
    print(log)


"""
function prepareHexPacket(destDev,sourceDev,cmd,timestamp,queuePk) - Prepare a Hex packet

INPUT:
    destDev - destination device - integer
    sourceDev - source device - integer
    cmd - command - integer
    timestamp - integer
    queuePk - input queue - queue of integers

OUTPUT:
    packet - Hex packet

"""

def prepareHexPacket(destDev,srcDev,cmd,timestamp,queuePk):
    packet = b""

    if cmd==cSpkRes and len(queuePk)==1:
#String: XX-XX-XX-XX-16 -XX-XX-XX-XX-XX-XX-XX-XX-00-00-00-01-XX-XX-XX
#Destination Device: XX-XX // destination device
#Source Device: XX-XX // source device
#Command: 16 // Spiking Neuron results
#Actual timestamp: XX-XX-XX-XX-XX-XX-XX-XX
#Payload Bytes: 00-00-00-01
#Spikes: XX
#Number of bytes: 18
        spike = queuePk.popleft()
        payload = struct.pack(">L", 1)
        packet+=destDev+srcDev+cmd+timestamp+payload+spike

    
    elif cmd==cMuscleRes and len(queuePk)==1:
#String: XX-XX-XX-XX-17-XX-XX-XX-XX-XX-XX-XX-XX-XX-00-01-XX-XX
#Destination Device: XX-XX // destination device
#Source Device: XX-XX // source device
#Command: 17 // muscle results
#Actual timestamp: XX-XX-XX-XX-XX-XX-XX-XX
#Payload Bytes: 00-00-00-04
#Force Value: XX-XX-XX-XX
#Number of bytes: 21
        payload = struct.pack(">L", 4)
        mForces = queuePk.popleft()
        packet+=destDev+srcDev+cmd+timestamp+payload+mForces
    
    elif cmd==cRTWResults and len(queuePk)==2:
#String: XX-XX-XX-XX-04-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-??
#Destination Device: XX-XX // destination device
#Source Device: XX-XX // source device
#Command: 04 // RTW result
#Timestamp: XX-XX-XX-XX-XX-XX-XX-XX
#Payload Bytes: XX-XX-XX-XX
#Variable id #: XX-XX
#Item Value: XX-XX-XX-XX // if some of the bytes are not used then fill those bytes with x00
#…
#Number of bytes: 23+6k //k is an integer greater or equal to 0
        items=queuePk.popleft() # vector of integers
        values=queuePk.popleft() # vector of integers
        payload=len(items)*2+len(values)*4
        payload = struct.pack(">L",payload)
        pck=b""
        for i in range(0,len(items),1):
            pck+=items[i]+values[i]
        packet+=destDev+srcDev+cmd+timestamp+payload+pck
        del pck

    return packet
