# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 16:43:44 2016

@author: pedromachado
"""


#For: Python 3.5
from urllib3 import filepost    #installed easy_install urllib3
from urllib.parse import urlencode
import http.client as httplib
import struct
import json
import math
import sys

from testClientFunctions import *

conn = httplib.HTTPConnection('100.100.1.104:443')

def QueryServiceAvailability():
	#(1) Example QueryServiceAvailability GET Request
	conn.request("GET", "/NUIG_RUS/QueryServiceAvailability")
	response = conn.getresponse()
	#print(response.status, response.reason)
	responseData = response.read()    #If 'Availability == true' received, ok to transmit
	#print(responseData)
	return response.status == 200
#######################################################################################



#function sendSingleRTWInitPacket(rtwId,simId,beginRTWTs,endRTWTs,tsSize,tsSampInterval,neuronId,neuronVariablesBeingRecorded)
# function arguments:
#    simId: Id for the current simulation in string format
#    rtwId: rtwId for the current rtw in string format
#    beginRTWTs: timestamp of the start of this recording to be transferred (number)
#    endRTWTs:  timestamp of the end of this recording to be transferred (number)
#    tsSize:  timestep size as a number (in seconds)
#    tsSampInterval:  number of timestamps between two recorded values (number)
#    neuronId : neuronId for the current neuron in string format
#    neuronVariablesBeingRecorded: list of strings of the names of variables being recorded
# does not return anything, however will raise exceptions if an error occurs during the server request or if a data error is caused
def sendSingleRTWInitPacket(rtwId,simId,beginRTWTs,endRTWTs,tsSize,tsSampInterval,neuronId,neuronVariablesBeingRecorded):
    #Create RTW Header XML from above data
    rtwHeaderXmlStr = createRTWXMLHeader(rtwId,simId,beginRTWTs,endRTWTs,tsSize,tsSampInterval,neuronId,neuronVariablesBeingRecorded)
    #print(rtwHeaderXmlStr)
    #printPrettyXML(rtwHeaderXmlStr)

    #Send/POST rtwHeaderXmlStr XML Header to the server (POST Request with plain text data)
    data = rtwHeaderXmlStr
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

    urlencodedStr = urlencode({'rNum':str(rtwId)})
    conn.request("POST", "/NUIG_RUS/variableRTWHeaderUpload/"+str(1),data,headers)
    response = conn.getresponse()
    #print(response.status, response.reason)
    responseData = response.read()
    #print(responseData)
    if not response.status == 200:
        raise ValueError('Error Occurred while sending RTW Init Packet Server Side: ', responseData)
    print('sendSingleRTWInitPacket complete for simId:' + str(simId) + ' for neuronid : ' + str(neuronId))


#function sendSingleRTWDataPacket(simId,neuronId,rtwId,neuronVariablesBeingRecorded,recordedData,recordingStart,recordingEnd)
# function arguments:
#    simId: Id for the current simulation in string format
#    simId: neuronId for the current neuron in string format
#    simId: rtwId for the current rtw in string format
#    neuronVariablesBeingRecorded: list of strings of the names of variables being recorded
#    recordedData: list of lists of floating point variable recordings, same order as above argument
#    recordingStart: timestamp of the start of this recording to be transferred (number)
#    recordingEnd:  timestamp of the end of this recording to be transferred (number)
# does not return anything, however will raise exceptions if an error occurs during the server request or if a data error is caused
def sendSingleRTWDataPacket(simId,neuronId,rtwId,neuronVariablesBeingRecorded,recordedData,recordingStart,recordingEnd):

    varDataXmlStr = createVarDataXMLHeader(simId,neuronId,rtwId,recordingStart,recordingEnd)    #Create Header for transmission of Timestep Variable Data
    #printPrettyXML(varDataXmlStr)
    stepLengthBytes = (8 + 4 * len(neuronVariablesBeingRecorded))
    totalLenth = (recordingEnd-recordingStart + 1)*stepLengthBytes
    dataBytes = bytearray(totalLenth);
    for i in range(0,recordingEnd-recordingStart+1):
        tsIdx = struct.pack('Q', recordingStart + i)    #Convert timestep 0 Index to double (8-byte) precision
        dataBytes[i*stepLengthBytes] = tsIdx[0]
        dataBytes[i*stepLengthBytes+1] = tsIdx[1]
        dataBytes[i*stepLengthBytes+2] = tsIdx[2]
        dataBytes[i*stepLengthBytes+3] = tsIdx[3]
        dataBytes[i*stepLengthBytes+4] = tsIdx[4]
        dataBytes[i*stepLengthBytes+5] = tsIdx[5]
        dataBytes[i*stepLengthBytes+6] = tsIdx[6]
        dataBytes[i*stepLengthBytes+7] = tsIdx[7]
        for j in range(0,len(neuronVariablesBeingRecorded)):
            number = recordedData[i][j]
            pi = struct.pack('f', number)    #Convert pi to floating point (4-byte) precision
            #dataBytes[i*stepLengthBytes + j*4:i*stepLengthBytes+ j*4 + 3] = [pi[0],pi[1],pi[2],pi[3]]
            dataBytes[i*stepLengthBytes + 8 + j*4] = (pi[0])
            dataBytes[i*stepLengthBytes + 8 + j*4 + 1] =(pi[1])
            dataBytes[i*stepLengthBytes + 8 + j*4 + 2] = (pi[2])
            dataBytes[i*stepLengthBytes + 8 + j*4 + 3] = (pi[3])

    #Error check that number of bytes in dataBytes is correct and corresponds to header
    errorCheckNumOfVars(neuronVariablesBeingRecorded, dataBytes, recordingStart, recordingEnd)    #for error checking

    dataBlobFields = (    #combining XML header and binary blob into HTTP packet
                          ('h', varDataXmlStr),    #header
                          ('b', dataBytes)        #bytes
                          )

    #Generate Multipart HTTP Header information and payload
    body, content_type  = filepost.encode_multipart_formdata(dataBlobFields)

    #Create HTTP header for packet
    headers = {'Content-Type': content_type,'content-length': str(len(body))}

    #POST HTTP Multipart payload and header to the server
    conn.request("POST", "/NUIG_RUS/variableResultsUpload/"+str(rtwId),body,headers)

    response = conn.getresponse()
    #print(response.status, response.reason)
    data = response.read()
    #print(data)
    conn.close()
    if not response.status == 200:
        raise ValueError('Error Occurred while sending RTW data on the Server Side: ' + data)
    print('sendSingleRTWDataPacket complete for simId:' + str(simId) + ' from: ' + str(recordingStart) + ' to ' + str(recordingEnd))


def sendNeuronData(simId,neuronId,variables,dataLength):

    rtwId = neuronId;        #RTW Number the header pertains to
    beginRTWTs = 0;        #The timeStep the RTW begins on
    tsSize = 0.005;        #the timeStep size (in seconds)
    endRTWTs = (int)(dataLength/tsSize);        #The timeStep the RTW ends on
    tsSampInterval = 1;        #how regularly the current Ts is being recorded

    #This is an array corresponding to the variables (items) being recorded for the neuron
    neuronVariablesBeingRecorded = variables    #for neuron 4

    sendSingleRTWInitPacket(rtwId,simId,beginRTWTs,endRTWTs,tsSize,tsSampInterval,neuronId,neuronVariablesBeingRecorded)
    #######################################################################################

    #(3) Upload data from timesteps to server using a combination of XML and binary data integrated into multipart_formdata
    #First construct the RTW Data Blob Header
    beginTs = 0;
    endTs = endRTWTs;


    #Create an example of the binary blob to be transferred in the payload of the HTTP packet
    ts0Idx = struct.pack('Q', 0)    #Convert timestep 0 Index to double (8-byte) precision
    #print('ts0Idx: ' + str(ts0Idx) + ' ,len:' + str(len(ts0Idx)))
    ts1Idx = struct.pack('Q', 1)    #Convert timestep 1 Index to double(8-byte) precision
    #print('ts1Idx: ' + str(ts1Idx) + ' ,len:' + str(len(ts1Idx)))
    pi = struct.pack('f', 3.141592654)    #Convert pi to floating point (4-byte) precision
    #print('pi: ' + str(pi) + ' ,len:' + str(len(pi)))
    #d = struct.unpack('f', 'bbbbbbbb'.decode('hex'))     #code to go from hex back to float/double
    #print(d)

    #Next construct datablob to be sent to the server
    #Data blob consists of: (a) 8 byte timeStep followed by (b) variable data from neuronVariablesBeingRecorded
    #    where each variable is represented by 4 bytes (floating-point precision)


    recordedData = []
    for i in range(0,endRTWTs+1):
        tsIdx = struct.pack('Q', i)    #Convert timestep 0 Index to double (8-byte) precision
        recordedData.append([])
        Fs=8000
        f=500
        for j in range(0,len(neuronVariablesBeingRecorded)):
            recordedData[i].append(math.sin(2*3.14*f*i/Fs))

    sendSingleRTWDataPacket(simId,neuronId,rtwId,neuronVariablesBeingRecorded,recordedData,beginRTWTs,endRTWTs)
    print('sendNeuronData complete for neuron: ' + str(neuronId) + ' for simId:' + str(simId))


#function sendSpikeData(simId, spikeBytes)
# function arguments:
#    simId: Id for the current simulation in string format
#    spikeBytes: bytearray of the spikes to be transferred, each spike is formed by 10 bytes of which 8 are for the timestamp and 2 for the id of the neuron that spiked
# does not return anything, however will raise exceptions if an error occurs during the server request or if a data error is caused
def sendSpikeData(simId, spikeBytes):
    beginTs = 0;
    endTs = 7;
    spikeDataXmlStr = createSpikeDataXMLHeader(simId,beginTs,endTs)    #Create Header for transmission of Spike Data
    #printPrettyXML(spikeDataXmlStr)


    #Error check that number of bytes in spikeBytes is correct and corresponds to header
    errorCheckSpikeBytes(spikeBytes, beginTs, endTs)    #for error checking

    spikeBlobFields = (    #combining XML header and binary blob into HTTP packet
        ('h', spikeDataXmlStr),    #header
        ('b', spikeBytes)        #bytes
    )

    #Generate Multipart HTTP Header information and payload
    body, content_type  = filepost.encode_multipart_formdata(spikeBlobFields)

    #Create HTTP header for packet
    headers = {'Content-Type': content_type,'content-length': str(len(body))}

    #POST HTTP Multipart payload and header to the server
    conn.request("POST", "/NUIG_RUS/spikeDataResultsUpload/",body,headers)

    response = conn.getresponse()
    #print(response.status, response.reason)
    data = response.read()
    #print(data)
    #print('(4) completed ####################################################')
    if not response.status == 200:
        raise ValueError('Error Occurred sending spike data packet on the Server Side: ' + data)
    print('spike data packet send for simId:' + str(simId))

def sendUploadCompletedNotice(simId):
    conn.request("GET", "/NUIG_RUS/uploadCompleted/simId=" + simId)
    response = conn.getresponse()
    #print(response.status, response.reason)
    data = response.read()
    #print(data)
    if not response.status == 200:
        raise ValueError('Error Occurred sending upload completed packet on the Server Side: ' + data)
