import time
import os
import manageCommands as mc
import downloadManager as dm
import numpy as np
import random
import struct
import queue
import RTWclient as RUS
import numpy as np


#check that the server is available
if not RUS.QueryServiceAvailability():
	raise ValueError('Service is not available')

simId = "pedro3";
numberOfNeurons = 5;
length = 100
for i in range(1, numberOfNeurons + 1):
    # sendNeuronData is an example of the sending of rtw results data to RUS for a single neuron
    # internally sendNeuronData calls
    #    sendSingleRTWInitPacket(rtwId,simId,beginRTWTs,endRTWTs,tsSize,tsSampInterval,neuronId,neuronVariablesBeingRecorded)
    #    and
    #    sendSingleRTWDataPacket(simId,neuronId,rtwId,neuronVariablesBeingRecorded,recordedData,beginRTWTs,endRTWTs)
    RUS.sendNeuronData(simId, i, ["a", "b", "c", "d"], length)

spikeBytes = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00,  # Timestep Index 0
                        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00,  # Timestep Index 0
                        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00,  # Timestep Index 0
                        0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00,  # Timestep Index 5
                        0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00,  # Timestep Index 6
                        0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00,  # Timestep Index 7
                        ])

# sendSpikeData(simId, spikeBytes) transfers the spike data, this must happen after the first rtw data has been transferred. (any amount of rtw data will do)
# NOTE: this function can be called any number of times with new data, but should never send the same spike twice for any simulation.
RUS.sendSpikeData(simId, spikeBytes);

# sendUploadCompletedNotice(simId) is a function that informs the server that the upload is complete for a particular simid, and the RUS will then notify the SC that the upload is complete

# function sendUploadCompletedNotice(simId)
# function arguments:
#    simId: Id for the current simulation in string format
RUS.sendUploadCompletedNotice(simId);