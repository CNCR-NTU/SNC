# -*- coding: utf-8 -*-
"""
Created on Fri Sep 2 18:23:44 2016

@author: pedromachado
"""

MCversion=1.1 #MC version

import time
import manageCommands as mc
import downloadManager as dm
import random
import struct
import queue
import RTWclient as RUS
import numpy as np
import serial
import fixed2float as f2f

global flag, numStim, spkCount
numStim=17
flag=False
fpgaflag=False
serialport='/dev/ttyS4'
spkCount = 0


qo=queue.Queue()
qi=queue.Queue()
qRUSi=queue.Queue()
qRUSo=queue.Queue()
qIMi=queue.Queue()
qIMo=queue.Queue()

class simulation:
    def __init__(self, simid, simtimestepsize, cyclesnum, timeout, timestamp):
        self.simid = simid
        self.simtimestepsize = simtimestepsize
        self.cyclesnum = cyclesnum
        self.timeout = timeout
        self.timestamp=timestamp

    def ls_sim(self):
        return [self.simid, self.simtimestepsize, self.cyclesnum, self.timeout, self.timestamp]

    def inc_timestamp(self,timestamp):
        self.timestamp = timestamp

    def __del__(self):
        print("Deleting simulation ", self.simid, " related data.")

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class modelController:
    def __init__(self,  nmid, modelid, nmtimestepsize):
        self.nmid = nmid
        self.modelid = modelid
        self.nmtimestepsize = nmtimestepsize
        self.mapSBs = b""
        self.nettopology=b""
        self.parametersvariables = [] # [itemId, itemType, itemDataType, itemIntegerPart, inLSB, inMSB, outLSB, outMSB, value]
        self.rtw = [] # [startTmstp, endTmstp, SamplingPeriod, [itemId1 .. itemIdn]]

    def ls_nm(self):
        return [self.nmid, self.modelid, self.nmtimestepsize, self.nettopology, self.mapSBs]

    def get_index(self, itemId):
        flag=False
        index=0
        for i in range(0,len(self.parametersvariables),1):
            tmp=self.parametersvariables[i]
            if tmp[0]==itemId:
                flag=True
                index=i
                break
        return flag,index

    #################################################################################
    def set_pv (self, id, parametersvariables):
        if self.nmid==id and len(parametersvariables)==9:
            self.parametersvariables.append(parametersvariables)# [itemId, itemType, itemDataType, itemIntegerPart, inLSB, inMSB, outLSB, outMSB, value]
            return True
        else:
            return False

    def get_pv(self, index):
        if index<len(self.parametersvariables):
            return self.parametersvariables[index]  # [itemId, itemType, itemDataType, itemIntegerPart, inLSB, inMSB, outLSB, outMSB, value]
        else:
            return []

    def ls_pv (self):
        return self.pv # [itemId, itemType, itemDataType, itemIntegerPart, inLSB, inMSB, outLSB, outMSB, value]


    def ls_size_pv(self):
        return len(self.parametersvariables)

    #################################################################################
    def set_rtw (self, id, rtw):
        if self.nmid==id:
            self.rtw=rtw # [startTmstp, endTmstp, SamplingPeriod, [itemId1 .. itemIdn]]
            return True
        else:
            return False

    def get_rtw  (self, index):
        if index<len(self.rtw):
            tmp=self.rtw[index] # [startTmstp, endTmstp, SamplingPeriod, [itemId1 .. itemIdn]]
            return tmp
        else:
            return []

    def ls_rtw (self):
        return self.rtw # [startTmstp, endTmstp, SamplingPeriod, [itemId1 .. itemIdn]]

    def ls_size_rtw(self):
        return len(self.rtw)

    #################################################################################

    def set_net (self, id, nettopology):
        if self.nmid==id:
            self.nettopology=nettopology # 38 bytes using one hot representation
            return True
        else:
            return False

    #################################################################################

    def set_mapsbs (self, id, mapsbs):
        if self.nmid==id:
            self.mapSBs=mapsbs # 38 bytes using one hot representation
            return True
        else:
            return False

    #################################################################################
    def __del__(self):
        print("Deleting simulation related data, for neuron/muscle ", self.nmid, " !")

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class stimulus:
    def __init__(self,  id):
        self.nmid = id
        self.configuredStim = []
        self.preconfstim = []  # [startTmstp, endTmstp, itemId, value A, Value B, Value C]
        self.runtimestim = []  # [itemID, value]

    #################################################################################
    def set_configuredStim(self, id, itemId):
        if self.nmid ==id:
            self.configuredStim.append(itemId)
            return True
        else:
            return False

    def ls_configuredStim(self):
        return self.configuredStim

    def ls_size_configuredStim(self):
        return len(self.configuredStim)

    #################################################################################

    def set_pcs(self, id, preconfstim):
        if self.nmid == id and len(preconfstim)==6:
            self.preconfstim.append(preconfstim)   # [startTmstp, endTmstp, itemId, value A, Value B, Value C]
            return True
        else:
            return False

    def get_pcs(self, index):
        return self.preconfstim[index]   # [startTmstp, endTmstp, itemId, value A, Value B, Value C]

    def ls_pcs(self):
        return self.preconfstim   # [startTmstp, endTmstp, itemId, value A, Value B, Value C]

    def ls_size_pcs(self):
        return len(self.preconfstim)

    #################################################################################

    def push_rts(self, id, rts):
        if self.nmid == id and len(rts)==2:
            self.runtimestim.append(rts)  # [itemID, value]
            return True
        else:
            return False

    def pop_rts(self):
        if len(self.runtimestim)>0:
            return self.runtimestim.pop(len(self.runtimestim)-1)  # [itemID, value]
        else :
            return []

    def ls_size_rts(self):
        return len(self.runtimestim)


    #################################################################################

    def __del__(self):
        print("Deleting simulation stimulus related data, for neuron/muscle ", self.nmid, " !")

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class results:
    def __init__(self,  id):
        self.modelid = id
        self.rtwvalues = [] # [itemid, timestamp, value]
        self.spikesforces = [] # [timetamp, spikes/forces]

    def push_rtwresults(self, rtwvalues):
        self.rtwvalues.append(rtwvalues) # [itemid, timestamp, value]

    def pop_rtwresuts(self):
        if len(self.rtwvalues)>0:
            return self.rtwvalues.pop(len(self.rtwvalues)-1)
        else:
            return []

    def ls_size_rtwresults(self):
        return len(self.rtwvalues)

    #################################################################################

    def push_sfresults(self, id, sfvalues):
        if self.nmid == id:
            self.spikesforces.append(sfvalues) # [timetamp, spikes/forces]
            return True
        else:
            return False

    def pop_sfresuts(self):
        if len(self.spikesforces) > 0:
            return self.spikesforces.pop(len(self.spikesforces) - 1)
        else:
            return []

    def ls_size_sfresults(self):
        return len(self.spikesforces)

    #################################################################################

    def __del__(self):
        print("Deleting simulation results related data, for neuron/muscle ", self.nmid, " !")


def MC(qi,qo):
    global flag, numStim
    ptimestamp=0
    simConfFlag = False
    confFlag=False
    # Only used for producing fake data
    muscleSync = 49
    muscleSyncCount=0
    rtwFlag = False
    neuronFlag=False
    stimFlag=False
    ids=[]
    muscleCount =0
    muscles=[]
    res = []
    while flag == True:
        if qi.empty() == False:
            aux = qi.get()
            qi.task_done()
            if len(aux) == 1:
                ax = aux[0]
                if ax == "start":
                    log = "[NM - " + time.strftime("%d/%m/%Y %H:%M:%S") + "] The NM service is now online!"
                    print(log)
                elif len(ax)==1:
                    if ax==struct.pack(">B",255):
                        print("Hello World")
                elif len(ax)>=17:
                    if ax[4:5] == mc.cConfSim and struct.unpack(">L", ax[13:17])[0] == 25: # validated!
                        # String: 00-00-XX-XX-00-00-00-00-00-00-00-00-00-19-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX
                        # Destination Device: 00-00 // broadcast [0:2]
                        # Source Device: XX-XX // source device [2:4]
                        # Command: 0E // initialize simulation parameters [4:5]
                        # Timestamp: 00-00-00-00-00-00-00-00 [5:13]
                        # Payload Bytes: 00-00-00-19 [13:17]
                        # Time step size: XX-XX-XX-XX [17:21]
                        # Number of cycles: XX-XX-XX-XX-XX-XX-XX-XX [21:29]
                        # Simulation ID: XX-XX-XX-XX-XX-XX-XX-XX [29:37]
                        # Timeout Period: XX-XX // in ms [37:39]
                        # Number of neurons: XX-XX // 0..302 [39:41
                        # Number of muscles: XX // 0 to 135 [41:42]
                        # Number of bytes: 42
                        log = "[NM - " + time.strftime("%d/%m/%Y %H:%M:%S") + "] A config simulation has been received!"
                        print(log)
                        sim=simulation(ax[29:37],ax[17:21],ax[21:29],ax[37:39],ax[5:13]) #simid, simtimestepsize, cyclesnum, timeout, timestamp
                        ## Test bench
                        # print("Number of Cycles", struct.unpack(">Q",ax[21:29])[0])
                        # print("Simulation ID: ", struct.unpack(">Q",ax[29:37])[0])
                        # print("Simulation time step size: ", struct.unpack(">f", ax[17:21])[0])
                        # print("Timeout: ", struct.unpack(">H", ax[37:39])[0])
                        # print("Timestamp :", struct.unpack(">Q", ax[5:13])[0])
                        # print("Simulation details:", sim.ls_sim(ax[29:37]))
                        simConfFlag=True

                    elif ax[4:5] == mc.cInitNeuron and np.mod((struct.unpack(">L", ax[13:17])[0]-6),25) == 0:
                        # String: XX-XX-XX-XX-18-00-00-00-00-00-00-00-00-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-??
                        # Destination Device: XX-XX // destination device [0..2]
                        # Source Device: XX-XX // source device [2..4]
                        # Command: 18 // Initialise neuron items [4..5]
                        # Timestamp: 00-00-00-00-00-00-00-00 [5..13]
                        # Payload Bytes: XX-XX-XX-XX [13..17]
                        # Model ID: XX-XX [17..19]
                        # Time Step size: XX-XX-XX-XX // in us [19..23]
                        # Item 1 id: XX-XX // same order as defined on the metadata file [23..25]
                        # Item 1 type: XX //1-parameter, 2-variable [25..26]
                        # Item 1 Data type: XX // see Table 7 [26..27]
                        # Item 1 integer part: XX // number of bits of the decimal part [27..28]
                        # Item 1 input BUS address LSB: XX-XX-XX-XX //size of 32 bits [28..32]
                        # Item 1 input BUS address MSB: XX-XX-XX-XX //size of 32 bits [32..36]
                        # Item 1 output BUS address LSB: XX-XX-XX-XX //size of 32 bits, set to 00-00-00-00 if it is a parameter [36..40]
                        # Item 1 output BUS address MSB: XX-XX-XX-XX //size of 32 bits, set to 00-00-00-00 if it is a parameter [40..44]
                        # Item 1 value: XX-XX-XX-XX // if some of the bytes are not used then fill those bytes with x00 [44..48]
                        # …
                        # Item n id: XX-XX // same order as defined on the metadata file
                        # Item n type: XX //1-parameter, 2-variable
                        # Item n Data type: XX // see Table 7
                        # Item n integer part: XX // number of bits of the decimal part
                        # Item n input BUS address LSB: XX-XX-XX-XX //size of 32 bits
                        # Item n input BUS address MSB: XX-XX-XX-XX //size of 32 bits
                        # Item n output BUS address LSB: XX-XX-XX-XX //size of 32 bits, set to 00-00-00-00 if it is a parameter
                        # Item n output BUS address MSB: XX-XX-XX-XX //size of 32 bits, set to 00-00-00-00 if it is a parameter
                        # Item n value: XX-XX-XX-XX // if some of the bytes are not used then fill those bytes with x00
                        # Number of bytes: 48+25k bytes// k is an integer greater or equal to 0
                        log = "[NM - " + time.strftime("%d/%m/%Y %H:%M:%S") + "] A neuron initialisation has been received!"
                        print(log)
                        tmp=struct.unpack(">H",ax[0:2])[0]
                        print("id",tmp)
                        if tmp>0 and tmp<303:
                            if muscleCount==0:
                                if neuronFlag==False or muscleCount==0:
                                    ids=[]
                                tmp=ax[0:2]
                                ids.append(tmp)
                                neuron=modelController(ax[0:2],ax[17:19],ax[19:23])
                                print(neuron.ls_nm())
                                res=stimulus(ax[0:2])
                                # send protect write packet to the FPGA
                                op = b"1"
                                nid=mc.mcIds[0]
                                command = mc.mcWrite + nid + op
                                command = struct.pack(">B", int(command, 2))
                                timestampf = ax[5:13]
                                timestepsize = ax[19:23]
                                model = ax[17:19]
                                packet = command + model + timestepsize + timestampf
                                log = "[NM - " + time.strftime(
                                    "%d/%m/%Y %H:%M:%S") + "] Packet protected write to be sent to FPGA:"+str(packet)
                                print(log)
                                if fpgaflag == True and len(packet)==15:
                                    try:
                                        ser = serial.Serial(serialport, 115200, timeout=1)
                                        log = "[NM - " + time.strftime(
                                            "%d/%m/%Y %H:%M:%S") + "] Sending protected write to FPGA"
                                        print(log)
                                        ser.flushInput()
                                        ser.flushOutput()
                                        ser.write(packet)
                                        ser.close()
                                    except serial.serialutil.SerialException:
                                        print("ERROR: The serial port is not available!")
                                op = b"1"
                                command = mc.mcWrite + mc.mcIds[0] + op
                                command = struct.pack(">B", int(command, 2))
                                packet = command + ax[17:19] + ax[19:23] + ax[5:13]
                                print("TO DO Send packet to FPGAs.\nPacket: ", packet)
                                iterations=int(((struct.unpack(">L",ax[13:17])[0])-6)/25)
                                for i in range(0,iterations,1):
                                    if int(struct.unpack(">H",ax[23+(i*25):25+(i*25)])[0]) > 65535 - numStim:
                                        if stimFlag==False:
                                            stim = stimulus(ax[0:2])
                                            stimFlag = True
                                        stim.set_configuredStim(ax[0:2],ax[23+(i*25):25+(i*25)])
                                        print("Stimulus #", numStim - 65535 + int(struct.unpack(">H", ax[23 + (i * 25):25 + (i * 25)])[0]),
                                          "initialised with success!")
                                    # [itemId, itemType, itemDataType, itemIntegerPart, inLSB, inMSB, outLSB, outMSB, value]
                                    neuron.set_pv(ax[0:2],[ax[23+(i*25):25+(i*25)],ax[25+(i*25):26+(i*25)],
                                    ax[26+(i*25):27+(i*25)],ax[27+(i*25):28+(i*25)],
                                    ax[28+(i*25):32+(i*25)],ax[32+(i*25):36+(i*25)],
                                    ax[36+(i*25):40+(i*25)],ax[40+(i*25):44+(i*25)],
                                    ax[44+(i*25):48+(i*25)]])
                                    # send standard write to the FPGA
                                    # standard write
                                    op = b"0"
                                    command = mc.mcWrite + nid + op
                                    command = struct.pack(">B", int(command, 2))
                                    lsb = ax[28 + (i * 25):32 + (i * 25)]
                                    msb = ax[32 + (i * 25):36 + (i * 25)]
                                    value = ax[44 + (i * 25):48 + (i * 25)]
                                    packet = command + lsb + msb + value
                                    log = "[NM - " + time.strftime(
                                        "%d/%m/%Y %H:%M:%S") + "] Packet standard write to be sent to FPGA:" + str(
                                        packet)
                                    print(log)
                                    if fpgaflag == True and len(packet) == 13:
                                        try:
                                            ser = serial.Serial(serialport, 115200, timeout=1)
                                            log = "[NM - " + time.strftime(
                                                "%d/%m/%Y %H:%M:%S") + "] Sending standard write #", i, "to FPGA"
                                            print(log)
                                            ser.flushInput()
                                            ser.flushOutput()
                                            ser.write(packet)
                                            ser.close()
                                        except serial.serialutil.SerialException:
                                            print("ERROR: The serial port is not available!")
                                confFlag = True
                                neuronFlag = True
                                # Restore state
                                op = b"0"
                                command = mc.mcRestoreState + nid + op
                                command = struct.pack(">B", int(command, 2))
                                packet = command
                                log = "[NM - " + time.strftime(
                                    "%d/%m/%Y %H:%M:%S") + "] Preparing restore state to FPGA"
                                print(log)
                                if fpgaflag == True and len(packet) == 15:
                                    try:
                                        ser = serial.Serial(serialport, 115200, timeout=1)
                                        log = "[NM - " + time.strftime(
                                            "%d/%m/%Y %H:%M:%S") + "] Sending restore state to FPGA"
                                        print(log)
                                        ser.flushInput()
                                        ser.flushOutput()
                                        ser.write(packet)
                                        ser.close()
                                    except serial.serialutil.SerialException:
                                        log = "[NM - " + time.strftime(
                                            "%d/%m/%Y %H:%M:%S") + "] ERROR: The serial port is not available!"
                                        print(log)
                            else:
                                print("TO DO generate error. muscle count:",muscleCount)
                        else:
                            print("TO DO generate error. Not in the range [1..302]", tmp)

                    elif ax[4:5] == mc.cIniMuscleIt and np.mod((struct.unpack(">L",ax[13:17])[0]-6),25)==0:
                        # String: XX-XX-XX-XX-14-00-00-00-00-00-00-00-00-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-??
                        # Destination Device: XX-XX // destination device
                        # Source Device: XX-XX // source device
                        # Command: 14 // Initialise muscle items
                        # Timestamp: 00-00-00-00-00-00-00-00
                        # Payload Bytes: XX-XX-XX-XX
                        # Model ID: XX-XX
                        # Time Step size: XX-XX-XX-XX // in us
                        # Item 1 id: XX-XX // same order as defined on the metadata file
                        # Item 1 type: XX //1-parameter, 2-variable
                        # Item 1 Data type: XX // see Table 7
                        # Item 1 integer part: XX // number of bits of the decimal part
                        # Item 1 input BUS address LSB: XX-XX-XX-XX //size of 32 bits
                        # Item 1 input BUS address MSB: XX-XX-XX-XX //size of 32 bits
                        # Item 1 output BUS address LSB: XX-XX-XX-XX //size of 32 bits, set to 00-00-00-00 if it is a parameter
                        # Item 1 output BUS address MSB: XX-XX-XX-XX //size of 32 bits, set to 00-00-00-00 if it is a parameter
                        # Item 1 value: XX-XX-XX-XX // if some of the bytes are not used then fill those bytes with x00
                        # …
                        # Item n id: XX-XX // same order as defined on the metadata file
                        # Item n type: XX //1-parameter, 2-variable
                        # Item n Data type: XX // see Table 7
                        # Item n integer part: XX // number of bits of the decimal part
                        # Item n input BUS address LSB: XX-XX-XX-XX //size of 32 bits
                        # Item n input BUS address MSB: XX-XX-XX-XX //size of 32 bits
                        # Item n output BUS address LSB: XX-XX-XX-XX //size of 32 bits, set to 00-00-00-00 if it is a parameter
                        # Item n output BUS address MSB: XX-XX-XX-XX //size of 32 bits, set to 00-00-00-00 if it is a parameter
                        # Item n value: XX-XX-XX-XX // if some of the bytes are not used then fill those bytes with x00
                        # Number of bytes: 48+25k bytes// k is an integer greater or equal to 0
                        log = "[NM - " + time.strftime("%d/%m/%Y %H:%M:%S") + "] A muscle initialisation has been received!"
                        print(log)
                        tmp=struct.unpack(">H",ax[0:2])[0]
                        if 302<tmp<438:
                            if neuronFlag==False:
                                if muscleCount<5:
                                    if neuronFlag == False or muscleCount == 0:
                                        ids = []
                                    ids.append(ax[0:2])
                                    muscles.append(modelController(ax[0:2],ax[17:19],ax[19:23]))
                                    res.append(stimulus(ax[0:2]))
                                    # send protect write packet to the FPGA
                                    op = b"1"
                                    mid=mc.mcIds[len(ids)-1]
                                    command = mc.mcWrite + mid + op
                                    command = struct.pack(">B", int(command, 2))
                                    print("Sending protected write: ", command)
                                    timestampf = ax[5:13]
                                    timestepsize = ax[19:23]
                                    model = ax[17:19]
                                    packet = command + model + timestepsize + timestampf
                                    log = "[NM - " + time.strftime(
                                        "%d/%m/%Y %H:%M:%S") + "] Packet protected write to be sent to FPGA:" + str(
                                        packet)
                                    print(log)
                                    if fpgaflag == True and len(packet)==15:
                                        try:
                                            ser = serial.Serial(serialport, 115200, timeout=1)
                                            log = "[NM - " + time.strftime(
                                                "%d/%m/%Y %H:%M:%S") + "] Sending protected write to FPGA"
                                            print(log)
                                            ser.flushInput()
                                            ser.flushOutput()
                                            ser.write(packet)
                                            ser.close()
                                        except serial.serialutil.SerialException:
                                            print("ERROR: The serial port is not available!")
                                    op = b"1"
                                    command = mc.mcWrite + mc.mcIds[muscleCount] + op
                                    command = struct.pack(">B", int(command, 2))
                                    packet = command+ax[17:19]+ax[19:23]+ax[5:13]
                                    print("TO DO Send packet to FPGAs.\nPacket: ", packet)
                                    iterations = int((struct.unpack(">L", ax[13:17])[0]) - 6 / 25)
                                    for i in range(0,iterations,1):
                                        # [itemId, itemType, itemDataType, itemIntegerPart, inLSB, inMSB, outLSB, outMSB, value]
                                        muscles[muscleCount].set_pv(ax[0:2],[ax[23+(i*25):25+(i*25)],ax[25+(i*25):26+(i*25)],
                                        ax[26+(i*25):27+(i*25)],ax[27+(i*25):28+(i*25)],
                                        ax[28+(i*25):32+(i*25)],ax[32+(i*25):36+(i*25)], # inLSB inMSB
                                        ax[36+(i*25):40+(i*25)],ax[40+(i*25):44+(i*25)], # outLSB outMSB
                                        ax[44+(i*25):48+(i*25)]]) # value
                                        # send normal write to the FPGA
                                        # standard write
                                        op = b"0"
                                        command = mc.mcWrite + mid + op
                                        command = struct.pack(">B", int(command, 2))
                                        lsb = ax[28+(i*25):32+(i*25)]
                                        msb = ax[32+(i*25):36+(i*25)]
                                        value=ax[44+(i*25):48+(i*25)]
                                        packet=command+lsb+msb+value
                                        log = "[NM - " + time.strftime(
                                            "%d/%m/%Y %H:%M:%S") + "] Packet standard write to be sent to FPGA:" + str(
                                            packet)
                                        print(log)
                                        if fpgaflag == True and len(packet)==13:
                                            try:
                                                ser = serial.Serial(serialport, 115200, timeout=1)
                                                log = "[NM - " + time.strftime(
                                                    "%d/%m/%Y %H:%M:%S") + "] Sending standard write #",i,"to FPGA"
                                                print(log)
                                                ser.flushInput()
                                                ser.flushOutput()
                                                ser.write(packet)
                                                ser.close()
                                            except serial.serialutil.SerialException:
                                                print("ERROR: The serial port is not available!")
                                    muscleCount += 1
                                    if confFlag == False:
                                        confFlag = True
                                    # Restore state
                                    op = b"0"
                                    command = mc.mcRestoreState + mid + op
                                    command = struct.pack(">B", int(command, 2))
                                    packet=command
                                    log = "[NM - " + time.strftime(
                                        "%d/%m/%Y %H:%M:%S") + "] Preparing restore state to FPGA"
                                    print(log)
                                    if fpgaflag == True and len(packet) == 15:
                                        try:
                                            ser = serial.Serial(serialport, 115200, timeout=1)
                                            log = "[NM - " + time.strftime(
                                                "%d/%m/%Y %H:%M:%S") + "] Sending restore state to FPGA"
                                            print(log)
                                            ser.flushInput()
                                            ser.flushOutput()
                                            ser.write(packet)
                                            ser.close()
                                        except serial.serialutil.SerialException:
                                            log = "[NM - " + time.strftime(
                                                "%d/%m/%Y %H:%M:%S") + "] ERROR: The serial port is not available!"
                                            print(log)

                            else:
                                print("TO DO generate error")
                        else:
                            print("TO DO generate error")
                    elif ax[4:5] == mc.cRTW and np.mod((struct.unpack(">L",ax[13:17])[0]-9),2)==0:
                        # String: XX-XX-XX-XX-10-XX-XX- XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-??
                        # Destination Device: XX-XX // destination device
                        # Source Device: XX-XX // source device
                        # Command: 10 // Define RTW
                        # Timestamp: XX-XX-XX-XX-XX-XX-XX-XX // start timestamp
                        # Payload Bytes: XX-XX-XX-XX
                        # End timestamp: XX-XX-XX-XX-XX-XX-XX-XX
                        # Sampling Period: XX // higher than 0 and lower than 255
                        # Variable 1 id: XX-XX // same order as specified in the metadata file
                        # …
                        # Variable n id: XX-XX // same order as specified in the metadata file
                        # Number of bytes:  28+2k bytes//k is an integer greater or equal to 0
                        if ids.count(ax[0:2])!=1:
                            print("ERROR: IDs not found!")
                        log = "[NM - " + time.strftime("%d/%m/%Y %H:%M:%S") + "] A rtw has been received!"
                        print(log)
                        iterator=(struct.unpack(">L",ax[13:17])[0]-9)/2
                        # [startTmstp, endTmstp, SamplingPeriod, [itemId1 .. itemIdn]]
                        item=[]
                        for i in range(0,iterator,1):
                            item.append(ax[26+(iterator*2):28+(iterator*2)])
                        neuron.set_rtw(ax[2:0],[ax[5:13],ax[17:25],ax[25:26],item])
                        if rtwFlag == False:
                            rtwFlag = True
                        del item

                    elif ax[4:5] == mc.cNewTmStp and struct.unpack(">L", ax[13:17])[0]==38:
                        # String: XX-XX-XX-XX-0D-00-00-XX-XX-XX-XX-XX-XX-00-00-00-26-XX-…-XX
                        # Destination Device: XX-XX // destination device [0:2]
                        # Source Device: XX-XX // source device [2:4]
                        # Command: 0D // New timestamp [4:5]
                        # New timestamp: XX-XX-XX-XX-XX-XX-XX-XX // timestamp+1
                        # Payload Bytes: 00-00-00-26
                        # Previous timestamp spikes: XX-…-XX // using one hot representation
                        log = "[NM - " + time.strftime("%d/%m/%Y %H:%M:%S") + "] A new timestamp command has been received!"
                        print(log)
                        if confFlag==True and simConfFlag==True:
                            # check
                            op=b"0"
                            command = mc.mcRunStep + mc.mcBid + op
                            command = struct.pack(">B", int(command, 2))
                            if neuronFlag==True:
                                if confFlag==True:
                                    if stimFlag==True:
                                        if stim.ls_size_pcs()>0:
                                            aux=stim.ls_pcs() # [startTmstp, endTmstp, value A, Value B, Value C]
                                            for i in range(0,stim.ls_size_pcs(),1):
                                                # [startTmstp, endTmstp, itemId, value A, Value B, Value C]
                                                log = "[NM - " + time.strftime(
                                                    "%d/%m/%Y %H:%M:%S") + "] Processing preconfigured stimuli!"
                                                print(log)
                                                if struct.unpack(">Q",aux[i][0])[0]>=ptimestamp and struct.unpack(">Q",aux[i][1])[0]<=ptimestamp:
                                                    deltaT=ptimestamp-struct.unpack(">Q",aux[i][1])[0]
                                                    pcsStim=struct.unpack(">f",aux[i][3])[0]*deltaT**2+struct.unpack(">f",aux[i][4])[0]*deltaT+struct.unpack(">f",aux[i][5])[0]
                                                    pcsStim=struct.pack(">f",pcsStim)
                                                    # send standard write to the FPGA
                                                    # standard write
                                                    op = b"0"
                                                    nid=mc.mcIds[0]
                                                    command = mc.mcWrite + nid + op
                                                    command = struct.pack(">B", int(command, 2))
                                                    itFlag, tmp=neuron.get_index(aux[i][3])
                                                    if itFlag==True:
                                                        tmp=neuron.get_pv(tmp)
                                                        # [itemId, itemType, itemDataType, itemIntegerPart, inLSB, inMSB, outLSB, outMSB, value]
                                                        lsb = tmp[4]
                                                        msb = tmp[5]
                                                        value = pcsStim
                                                        packet = command + lsb + msb + value
                                                        log = "[NM - " + time.strftime(
                                                            "%d/%m/%Y %H:%M:%S") + "] Packet standard write to be sent to FPGA:" + str(
                                                            packet)
                                                        print(log)
                                                        if fpgaflag == True and len(packet) == 13:
                                                            try:
                                                                ser = serial.Serial(serialport, 115200, timeout=1)
                                                                log = "[NM - " + time.strftime(
                                                                    "%d/%m/%Y %H:%M:%S") + "] Sending standard write #", i, "to FPGA"
                                                                print(log)
                                                                ser.flushInput()
                                                                ser.flushOutput()
                                                                ser.write(packet)
                                                                ser.close()
                                                            except serial.serialutil.SerialException:
                                                                print("ERROR: The serial port is not available!")
                                                    else:
                                                        log = "[NM - " + time.strftime(
                                                            "%d/%m/%Y %H:%M:%S") + "] ERROR: Item not initialised!"
                                                        print(log)
                                        del aux
                                    if rtwFlag==True:
                                        print("TO DO Request rtw values from neuron, convert them and send them to RUS.")
                                        if neuron.ls_size_rtw()>0:
                                            aux = neuron.ls_rtw()
                                            # aux= [startTmstp, endTmstp, SamplingPeriod, [itemId1 .. itemIdn]]

                                            log = "[NM - " + time.strftime(
                                                "%d/%m/%Y %H:%M:%S") + "] Processing RTWs!"
                                            print(log)
                                            for i in range(0, neuron.ls_size_rtw(),1):
                                                if struct.unpack(">Q", aux[i][0])[0] >= ptimestamp and struct.unpack(">Q", aux[i][1])[0] <= ptimestamp:
                                                    items=aux[i][3]
                                                    for j in range(0,len(items),1):
                                                        # standard read
                                                        op=b'0'
                                                        nid = mc.mcIds[0]
                                                        command = mc.mcRead + nid + op
                                                        command = struct.pack(">B", int(command, 2))
                                                        itFlag, tmp = neuron.get_index(aux[i][3])
                                                        if itFlag==True:
                                                            tmp = neuron.get_pv(tmp)
                                                            # [itemId, itemType, itemDataType, itemIntegerPart, inLSB, inMSB, outLSB, outMSB, value]
                                                            datatype=struct.unpack(">B",tmp[2])[0]
                                                            lsb = tmp[6]
                                                            msb = tmp[7]
                                                            packet = command + lsb + msb
                                                            log = "[NM - " + time.strftime(
                                                                "%d/%m/%Y %H:%M:%S") + "] Packet standard read to be sent to FPGA:" + str(
                                                                packet)
                                                            print(log)
                                                            if fpgaflag == True and len(packet) == 9:
                                                                try:
                                                                    ser = serial.Serial(serialport, 115200, timeout=1)
                                                                    log = "[NM - " + time.strftime(
                                                                        "%d/%m/%Y %H:%M:%S") + "] Sending standard read # "+str(i)+" to FPGA"
                                                                    print(log)
                                                                    ser.flushInput()
                                                                    ser.flushOutput()
                                                                    ser.write(packet)
                                                                    print("Reading results")
                                                                    s = ser.read(5)
                                                                    # b”11100010”==226
                                                                    if struct.unpack(">B", s[0:1])[0] == 226:
                                                                        data=f2f.HexToDec(s[1:4],datatype)
                                                                        data=struct.pack(">f",data)
                                                                        results.push_rtwresults(tmp[0],struct.pack(">Q",ptimestamp+1), data)
                                                                    else:
                                                                        log = "[NM - " + time.strftime(
                                                                            "%d/%m/%Y %H:%M:%S") + "] ERROR. Wrong 1st byte number"+str(struct.unpack(">B", s[0:1])[0])
                                                                        print(log)
                                                                    ser.close()
                                                                except serial.serialutil.SerialException:
                                                                    log = "[NM - " + time.strftime(
                                                                        "%d/%m/%Y %H:%M:%S") + "] ERROR. ERROR: The serial port is not available!"
                                                                    print(log)

                                                            elif fpgaflag == False:
                                                                fakevalue = struct.pack(">f", np.random())
                                                                results.push_rtwresults(tmp[0],struct.pack(">Q",ptimestamp + 1),fakevalue)
                                                            # [itemid, timestamp, value]
                                                            tmp1=results.pop_rtwresuts()
                                                            # [simId, neuronId, startTimestamp, endTimestamp, rtwId, variableToUpload]
                                                            rtwpacket = [sim.ls_sim()[0], neuron.ls_nm()[0], tmp1[0], tmp1[0], tmp1[1], tmp1[2]]
                                                            qRUSi.put(["rtwRes", rtwpacket])
                                                            print(" Sending fake RTW to RUS")
                                                        else:
                                                            log = "[NM - " + time.strftime(
                                                                "%d/%m/%Y %H:%M:%S") + "] ERROR: Item not initialised!"
                                                            print(log)
                                # send new timestamp to the FPGA
                                op = b"0"
                                nid = mc.mcIds[0]
                                command = mc.mcRunStep + nid + op
                                command = struct.pack(">B", int(command, 2))
                                spikes = ax[17:55]
                                packet=command+spikes
                                log = "[NM - " + time.strftime(
                                    "%d/%m/%Y %H:%M:%S") + "] Packet standard write to be sent to FPGA:" + str(
                                    packet)
                                print(log)
                                if fpgaflag == True and len(packet) == 39:
                                    try:
                                        ser = serial.Serial(serialport, 115200,
                                                            timeout=1)
                                        log = "[NM - " + time.strftime(
                                            "%d/%m/%Y %H:%M:%S") + "] Sending standard write #", i, "to FPGA"
                                        print(log)
                                        ser.flushInput()
                                        ser.flushOutput()
                                        ser.write(packet)
                                        s = ser.read(1)
                                        ser.close()
                                        res = struct.unpack(">B", s[0:1])[0]
                                        if res == 98:
                                            spk = struct.pack(">B",0)
                                        elif res == 99:
                                            spk = struct.pack(">B", 1)
                                        else:
                                            spk = struct.pack(">B", 0)
                                            log = "[NM - " + time.strftime(
                                                "%d/%m/%Y %H:%M:%S") + "] ERROR: Wrong Byte value [expected: 98 or 99]! "+str(res)
                                            print(log)
                                    except serial.serialutil.SerialException:
                                        spk = struct.pack(">B", 0)
                                        log = "[NM - " + time.strftime(
                                            "%d/%m/%Y %H:%M:%S") + "] ERROR: The serial port is not available!"
                                        print(log)
                                    # String: XX-XX-XX-XX-16 -XX-XX-XX-XX-XX-XX-XX-XX-00-00-00-01-XX-XX-XX
                                    # Destination Device: XX-XX // destination device
                                    # Source Device: XX-XX // source device
                                    # Command: 16 // Spiking Neuron results
                                    # Actual timestamp: XX-XX-XX-XX-XX-XX-XX-XX
                                    # Payload Bytes: 00-00-00-01
                                    # Spikes: XX
                                    # Number of bytes: 18
                                    destDev = mc.IMFPGA
                                    srcDev = ids[0]
                                    cmd = mc.cSpkRes
                                    payload = struct.pack(">I", 1)
                                    hexpacket = destDev + srcDev + cmd + ptimestamp + payload + spk
                                elif fpgaflag==False:
                                    hexpacket = generateNMdata(neuron.ls_nm()[0], ax[5:13])
                                qIMi.put(["spikeRes",hexpacket])
                            elif muscleCount > 0:
                                print("TO DO Send weights")
                                if muscleSyncCount==muscleSync:
                                    # testbench
                                    for i in range(0,muscleCount,1):
                                        # send new timestamp to the FPGA
                                        op = b"0"
                                        mid = mc.mcIds[i]
                                        command = mc.mcRunStep + mid + op
                                        command = struct.pack(">B", int(command, 2))
                                        spikes = ax[17:55]
                                        packet = command + spikes
                                        log = "[NM - " + time.strftime(
                                            "%d/%m/%Y %H:%M:%S") + "] Packet standard write to be sent to FPGA:" + str(
                                            packet)
                                        print(log)
                                        if fpgaflag == True and len(packet) == 39:
                                            try:
                                                ser = serial.Serial(serialport, 115200,
                                                                    timeout=1)
                                                log = "[NM - " + time.strftime(
                                                    "%d/%m/%Y %H:%M:%S") + "] Sending standard write #", i, "to FPGA"
                                                print(log)
                                                ser.flushInput()
                                                ser.flushOutput()
                                                ser.write(packet)
                                                s = ser.read(5)
                                                ser.close()
                                                if len(s)==5:
                                                    contraction = struct.unpack(">f", s[1:5])[0]
                                                else:
                                                    contraction=0.0
                                                if contraction<0.0:
                                                    contraction=0.0
                                                elif contraction>1.0:
                                                    contraction=1.0
                                            except serial.serialutil.SerialException:
                                                contraction = struct.pack(">B", 0)
                                                log = "[NM - " + time.strftime(
                                                    "%d/%m/%Y %H:%M:%S") + "] ERROR: The serial port is not available!"
                                                print(log)
                                            # testbench
                                            # String: XX-XX-XX-XX-17-XX-XX-XX-XX-XX-XX-XX-XX-XX-00-01-XX-XX
                                            # Destination Device: XX-XX // destination device
                                            # Source Device: XX-XX // source device
                                            # Command: 17 // muscle results
                                            # Actual timestamp: XX-XX-XX-XX-XX-XX-XX-XX
                                            # Payload Bytes: 00-00-00-04
                                            # Force Value: XX-XX-XX-XX
                                            # Number of bytes: 21
                                            destDev = mc.IMFPGA
                                            srcDev = ids[i]
                                            cmd = mc.cMuscleRes
                                            payload = struct.pack(">I", 4)
                                            hexPacket = destDev + srcDev + cmd + ptimestamp + payload + contraction
                                        elif fpgaflag== False:
                                            hexpacket = generateNMdata(muscles[i].ls_nm()[0],ax[5:13])
                                        qIMi.put(["muscleRes", hexpacket])
                                    muscleSyncCount =0
                                else:
                                    muscleSyncCount+=1
                            ptimestamp+=1
                            sim.inc_timestamp(struct.pack(">Q",ptimestamp))
                        else:
                            log = "[NM - " + time.strftime(
                                "%d/%m/%Y %H:%M:%S") + "] WARNING: New timestam ignored!"
                            print(log)
                        # check RTWs


                    elif ax[4:5] == mc.cConfigNetTop and int(struct.unpack(">L", ax[13:17])[0]) == 38:
                        # String: XX-XX-XX-XX-0B-XX-XX-XX-XX-XX-XX-XX-XX-00-00-00-26-XX-…-XX
                        # Destination Device: XX-XX // destination device
                        # Source Device: XX-XX // source device
                        # Command: 0B // Config network topology
                        # Timestamp: XX-XX-XX-XX-XX-XX-XX-XX // start timestamp
                        # Payload Bytes: 00-00-00-26
                        # Network topology: XX-…-XX // using one hot representation
                        # Number of bytes: 55 bytes
                        log = "[NM - " + time.strftime("%d/%m/%Y %H:%M:%S") + "] A config network topology command has been received!"
                        print(log)
                        if confFlag==True and neuronFlag==True:
                            log = "[NM - " + time.strftime(
                                "%d/%m/%Y %H:%M:%S") + "] A config network topology processed!"
                            neuron.set_net(ax[0:2],ax[17:55])
                            tmp = b"0001"
                        elif confFlag==True and muscleCount>0:
                            index=ids.index(ax[0:2])
                            tmp=mc.mcIds[index]
                            muscles[tmp].set_net(ax[0:2],ax[17:55])
                        log = "[NM - " + time.strftime(
                            "%d/%m/%Y %H:%M:%S") + "] A config network topology has been processed!"
                        print(log)
                        op=b"0"
                        command = mc.mcConfNetTop + tmp + op
                        command = struct.pack(">B", int(command, 2))
                        packet = command + ax[17:55]
                        print("TO DO Send packet to FPGAs.\nPacket: ", packet)

                    elif ax[4:5] == mc.cMapSBinput and int(struct.unpack(">L", ax[13:17])[0]) == 40:
                        # String: XX-XX-XX-XX-0B-XX-XX-XX-XX-XX-XX-XX-XX-00-00-00-26-XX-…-XX
                        # Destination Device: XX-XX // destination device
                        # Source Device: XX-XX // source device
                        # Command: 21 // Config network topology
                        # Timestamp: XX-XX-XX-XX-XX-XX-XX-XX // start timestamp
                        # Payload Bytes: 00-00-00-28
                        # Pre neuron ID 1: XX-XX
                        # …
                        # Pre neuron ID 20: XX-XX
                        # Number of bytes: 57 bytes
                        log = "[NM - " + time.strftime("%d/%m/%Y %H:%M:%S") + "] A map synaptic boards input has been received!"
                        print(log)
                        if confFlag==True and neuronFlag==True:
                            neuron.mapSBs(ax[0:2],ax[17:57])
                            tmp=b"0001"
                        elif confFlag == True and muscleCount > 0:
                            index=ids.index(ax[0:2])
                            tmp=mc.mcIds[index]
                            muscles[tmp].set_net(ax[0:2],ax[17:57])
                            log = "[NM - " + time.strftime(
                                "%d/%m/%Y %H:%M:%S") + "] A map synaptic boards input has been processed!"
                            print(log)
                        op=b"0"
                        command = mc.mcMapSBInput + tmp + op
                        command = struct.pack(">B", int(command, 2))
                        packet = command + ax[17:57]
                        print("TO DO Send packet to FPGAs.\nPacket: ", packet)

                    elif ax[4:5] == mc.cReset and int(struct.unpack(">L", ax[13:17])[0]) == 0:
                        # String: XX-XX-XX-XX-0F-XX-XX-XX-XX-XX-XX-XX-XX-00-00-00-00
                        # Destination Device: XX-XX // destination device
                        # Source Device: XX-XX // source device
                        # Command: 0F // reset simulation
                        # Timestamp: XX-XX-XX-XX-XX-XX-XX-XX
                        # Payload Bytes: 00-00-00-00
                        # Number of bytes: 17
                        if simConfFlag == True:
                            del sim
                            simConfFlag = False
                        if confFlag==True and neuronFlag == True:
                            del neuron
                            del ids
                            del res
                            neuronFlag = False
                        elif confFlag==True and muscleCount > 0:
                            muscleCount=0
                            del ids
                            for i in range(0, len(muscles), 1):
                                del muscles[i]
                                del stim[i]
                                del res[i]
                            del muscles
                            del stim
                            del res
                            muscleSyncCount = 0
                        confFlag = False
                        rtwFlag = False
                        stimFlag = False
                        ptimestamp=0
                        log = "[NM - " + time.strftime("%d/%m/%Y %H:%M:%S") + "] A reset command has been received!"
                        print(log)
                        op = b"0"
                        command = mc.mcReset + mc.mcBid + op
                        command = struct.pack(">B", int(command, 2))
                        if fpgaflag==True:
                            try:
                                ser = serial.Serial(serialport, 115200)
                                ser.flushInput()
                                ser.flushOutput()
                                ser.write(command)
                                ser.close()
                            except serial.serialutil.SerialException:
                                print("ERROR: The serial port is not available!")

                    elif ids.count(ax[0:2])==1 and ax[4:5] == mc.cPreconfStim and struct.unpack(">L", ax[13:17])[0] == 22:
                        # String: XX-XX-XX-XX-13-XX-XX-XX-XX-XX-XX-XX-XX-00-00-00-16-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX
                        # Destination Device: XX-XX // destination device
                        # Source Device: XX-XX // source device
                        # Command: 13 // preconfigured stimulus
                        # Timestamp: XX-XX-XX-XX-XX-XX-XX-XX // start timestamp
                        # Payload Bytes: 00-00-00-16
                        # End timestamp: XX-XX-XX-XX-XX-XX-XX-XX // end timestamp
                        # Item id: XX-XX // same order as defined on the metadata file
                        # Item value A: XX-XX-XX-XX // if some of the bytes are not used then fill those bytes with x00
                        # Item value B: XX-XX-XX-XX // if some of the bytes are not used then fill those bytes with x00
                        # Item value C: XX-XX-XX-XX // if some of the bytes are not used then fill those bytes with x00
                        # Number of bytes: 39 bytes
                        log = "[NM - " + time.strftime("%d/%m/%Y %H:%M:%S") + "] A preconfigured stimulus has been received!"
                        print(log)
                        if confFlag==True and simConfFlag==True:
                            if neuronFlag==True:
                                # [startTmstp, endTmstp, itemId, value A, Value B, Value C]
                                if neuron.check_itemId(ax[25:27])[0]==True:
                                    log = "[NM - " + time.strftime(
                                        "%d/%m/%Y %H:%M:%S") + "] A preconfigured processed!"
                                    stim.set_pcs(ax[0:2],[ax[5:13], ax[17:25],ax[25:27],ax[27:31],ax[31:35],ax[35:39]])
                                else:
                                    print("WARNING: Stimulus not initialised and therefore has been ignored.")
                            elif confFlag == True and muscleCount > 0:
                                print("TO DO Generate error!")
                        else:
                            print("TO DO Generate error!")

                    elif ids.count(ax[0:2]) == 1 and ax[4:5] == mc.cRuntimeStim and struct.unpack(">L", ax[13:17])[0] == 6:
                        # String: XX-XX-XX-XX-1A-XX-XX-XX-XX-XX-XX-XX-XX-00-00-00-06-XX-XX-XX-XX-XX-XX
                        # Destination Device: XX-XX // destination device
                        # Source Device: XX-XX // source device
                        # Command: 1A // runtime stimulus
                        # Timestamp: XX-XX-XX-XX-XX-XX-XX-XX // start timestamp
                        # Payload Bytes: 00-00-00-06
                        # Item id: XX-XX // same order as defined on the initialisation
                        # Item value: XX-XX-XX-XX // if some of the bytes are not used then fill those bytes with x00
                        # Number of bytes: 23 bytes
                        log = "[NM - " + time.strftime("%d/%m/%Y %H:%M:%S") + "] A runtime stimulus has been received!"
                        print(log)
                        if confFlag == True and simConfFlag == True:
                            if neuronFlag == True:
                                # [itemID, value]
                                stim.push_rts(ax[0:2], [ax[17:19], ax[19:23]])
                            else:
                                print("TO DO Generate error!")
                        else:
                            print("TO DO Generate error!")
    aux=qi.get()
    qi.task_done()
    ax=aux[0]
    if ax=="close":
        log="[NM - " + time.strftime("%d/%m/%Y %H:%M:%S")+"] Deleting simulation data from memory!"
        if simConfFlag == True:
            del sim
        if neuronFlag == True:
            del neuron
            del ids
            del res
        elif muscleCount>0:
            del ids
            for i in range(0,len(muscles),1):
                del muscles[i]
                del stim[i]
                del res[i]
            del muscles
            del stim
            del res


            print(log)

        log="[NM - " + time.strftime("%d/%m/%Y %H:%M:%S")+"] The NM service is shutting down..."
        print(log)
        qo.put("[NM - " + time.strftime("%d/%m/%Y %H:%M:%S")+"] The NM service is now closed!")

def RUS(qRUSi,qRUSo):
    global flag
    while flag==True:
        if qRUSi.empty()==False:
            aux=qRUSi.get()
            qRUSi.task_done()
            ax = aux[0]
            if len(aux)==1:
                if ax=="start":
                    log="[RUS - " + time.strftime("%d/%m/%Y %H:%M:%S")+"] The RUS service is now online!"
                    print(log)
            elif len(aux) == 2:
                if ax=="spikeRes" :
                    log = "[RUS - " + time.strftime("%d/%m/%Y %H:%M:%S") + "] Sending spike results to the RUS!"
                    print(log)
                    # TO DO implement behaviour
                elif ax=="rtwRes":
                    log = "[RUS - " + time.strftime("%d/%m/%Y %H:%M:%S") + "] Sending RTW results to the RUS!"
                    print(log)
                    # TO DO implement behaviour
                    # [simId, neuronId, startTimestamp, endTimestamp, rtwId, variableToUpload]
                    tmp=aux[1]
                    simId = struct.unpack(">Q", tmp[0])[0]
                    rtwId = struct.unpack(">H", tmp[4])[0]
                    neuronId = struct.unpack(">H", tmp[1])[0]
                    neuronVariablesBeingRecorded = [
                        1]  # this doesn't matter as long as the elements are same length as below
                    variableToUpload = tmp[5]
                    recordedData = [variableToUpload[0], variableToUpload[1], variableToUpload[2], variableToUpload[3]]
                    startTimeStep = struct.unpack(">Q", tmp[2])[0]
                    endTimeStep = struct.unpack(">Q", tmp[3])[0]  # start and end are the same if we are transferring one timestep data only
                    RUS.sendSingleRTWInitPacket(rtwId,simId,startTimeStep,endTimeStep,0.001,1,neuronId,neuronVariablesBeingRecorded)
                    RUS.sendSingleRTWDataPacket(simId, neuronId, rtwId, neuronVariablesBeingRecorded, recordedData,
                                            startTimeStep, endTimeStep)
    aux=qRUSi.get()
    qRUSi.task_done()
    ax=aux[0]
    if ax=="close":
        log="[RUS - " + time.strftime("%d/%m/%Y %H:%M:%S")+"] The RUS service is shutting down..."
        print(log)
        qRUSo.put("[RB - " + time.strftime("%d/%m/%Y %H:%M:%S")+"] The RB service is now closed!")


def IM(qIMi,qIMo):
    global flag
    while flag==True:
        if qIMi.empty()==False:
            aux=qIMi.get()
            qIMi.task_done()
            ax = aux[0]
            if len(aux)==1:
                if ax=="start":
                    log="[IM - " + time.strftime("%d/%m/%Y %H:%M:%S")+"] The IM service is now online!"
                    print(log)
            elif len(aux)==2:
                if ax=="spikeRes":
                    log = "[IM - " + time.strftime("%d/%m/%Y %H:%M:%S") + "] Sending pike results to the IM!"
                    print(log)
                    #dm.TCPclient(aux[1])
                    dm.UDPclient(aux[1])
                elif ax=="muscleRes":
                    log = "[IM - " + time.strftime("%d/%m/%Y %H:%M:%S") + "] Sending muscle results to the IM!"
                    print(log)
                    #dm.TCPclient(aux[1])
                    dm.UDPclient(aux[1])

    aux=qIMi.get()
    qIMi.task_done()
    ax=aux[0]
    if ax=="close":
        log="[IM - " + time.strftime("%d/%m/%Y %H:%M:%S")+"] The IM service is shutting down..."
        print(log)
        qIMo.put("[IM - " + time.strftime("%d/%m/%Y %H:%M:%S")+"] The IM service is now closed!")


"""
procedure generateNMdata(neuronMuscles,timestamp,qi) -generate fake Neurons and Muscles data

INPUT:
    neuronMuscles - vectors of integers
    timestamp - integer

OUTPUT:
    hex packet - queue input to the IMFPGA


"""


def generateNMdata(id,timestamp):
    global spkCount
    if len(id)>0:
        if 0<struct.unpack(">H",id)[0]<303:
            # String: XX-XX-XX-XX-16 -XX-XX-XX-XX-XX-XX-XX-XX-00-00-00-01-XX-XX-XX
            # Destination Device: XX-XX // destination device
            # Source Device: XX-XX // source device
            # Command: 16 // Spiking Neuron results
            # Actual timestamp: XX-XX-XX-XX-XX-XX-XX-XX
            # Payload Bytes: 00-00-00-01
            # Spikes: XX
            # Number of bytes: 18
            destDev = mc.IMFPGA
            srcDev = id
            cmd = mc.cSpkRes
            payload = struct.pack(">I", 1)
            if spkCount==0:
                spike=struct.pack(">B",random.randint(0,1))
            else:
                spkCount-=1
            if spike==1:
                spkCount=random.randint(10,50)
            hexPacket=destDev+srcDev+cmd+timestamp+payload+spike
            print(hexPacket)
            log="[IM td - " + time.strftime("%d/%m/%Y %H:%M:%S")+"] Neuron: "+str(struct.unpack(">H",id)[0])+", timestamp: "+str(timestamp)+ ", packet: "+str(hexPacket)
            print(log)
            return(hexPacket)
            #return hexPacket
            #time.sleep(0.001)
        else:
            # String: XX-XX-XX-XX-17-XX-XX-XX-XX-XX-XX-XX-XX-XX-00-01-XX-XX
            # Destination Device: XX-XX // destination device
            # Source Device: XX-XX // source device
            # Command: 17 // muscle results
            # Actual timestamp: XX-XX-XX-XX-XX-XX-XX-XX
            # Payload Bytes: 00-00-00-04
            # Force Value: XX-XX-XX-XX
            # Number of bytes: 21
            destDev = mc.IMFPGA
            srcDev = id
            cmd = mc.cMuscleRes
            force=struct.pack(">f",random.random())
            payload=struct.pack(">I",4)
            hexPacket=destDev+srcDev+cmd+timestamp+payload+force
            log="[IM td - "+ time.strftime("%d/%m/%Y %H:%M:%S")+"] Muscle: "+str(struct.unpack(">H",id)[0]-302)+", timestamp: " + str(timestamp) + ", packet: "+str(hexPacket)
            print(log)
            return(hexPacket)

def prepareSpkTrain(spks,net):
    res=b""
    for i in range(0,len(spks),1):
        if struct.unpack(">B",net[i])[0]>0:
            if struct.unpack(">B",spks[i])[0]>0:
                a=bin(struct.unpack(">B",net[i])).lstrip('0b')
                b=bin(struct.unpack(">B",spks[i])).lstrip('0b')
                tmp=''
                for j in range(0,len(a),1):
                    if a[j]=='1':
                        tmp+=b[j]
                    else:
                        tmp+='0'
                res+=struct.pack(">B",int(tmp,2))
            else:
                res += struct.pack(">B", 0)
        else:
            res += struct.pack(">B", 0)
    return res