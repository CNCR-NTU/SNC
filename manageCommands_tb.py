import manageCommands as mc
import id
import struct
from collections import deque

if __name__ == "__main__":
    destDev=mc.SC
    srcDev=id.nid[0]

    # String: XX-XX-XX-XX-04-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-??
    # Destination Device: XX-XX // destination device
    # Source Device: XX-XX // source device
    # Command: 04 // RTW result
    # Timestamp: XX-XX-XX-XX-XX-XX-XX-XX
    # Payload Bytes: XX-XX-XX-XX
    # Variable id #: XX-XX
    # Item Value: XX-XX-XX-XX // if some of the bytes are not used then fill those bytes with x00
    # …
    # Number of bytes: 23+6k //k is an integer greater or equal to 0
    com=mc.cRTWResults
    timestamp=struct.pack(">Q",10)
    queuePk=deque()
    items=[]
    values=[]
    for i in range (0,10,1):
        varId=struct.pack(">H",1)
        items.append(varId)
        itemVal=struct.pack(">f",1.0)
        values.append(itemVal)
    queuePk.append(items)
    queuePk.append(values)
    del items
    del values
    packet=mc.prepareHexPacket(destDev,srcDev,com,timestamp,queuePk)
    print("RTW result: ", packet, " length :", len(packet))

    # String: XX-XX-XX-XX-16 -XX-XX-XX-XX-XX-XX-XX-XX-00-00-00-01-XX-XX-XX
    # Destination Device: XX-XX // destination device
    # Source Device: XX-XX // source device
    # Command: 16 // Spiking Neuron results
    # Actual timestamp: XX-XX-XX-XX-XX-XX-XX-XX
    # Payload Bytes: 00-00-00-01
    # Spikes: XX
    # Number of bytes: 18
    com=mc.cSpkRes
    timestamp = struct.pack(">Q", 11)
    spikes=struct.pack(">B",1)
    queuePk.append(spikes)
    del spikes
    packet = mc.prepareHexPacket(destDev, srcDev, com, timestamp, queuePk)
    print("Spike results: ", packet, " length :", len(packet))

    # String: XX-XX-XX-XX-0D-00-00-XX-XX-XX-XX-XX-XX-00-00-00-26-XX-…-XX
    # Destination Device: XX-XX // destination device
    # Source Device: XX-XX // source device
    # Command: 0D // New timestamp
    # New timestamp: XX-XX-XX-XX-XX-XX-XX-XX // timestamp+1
    # Payload Bytes: 00-00-00-26
    # Previous timestamp spikes: XX-…-XX // using one hot representation
    com = mc.cNewTmStp
    timestamp = struct.pack(">Q", 11)
    spikes = b""
    for i in range(0, 38, 1):
        spikes += struct.pack(">B", i)
    queuePk.append(spikes)
    del spikes
    packet = mc.prepareHexPacket(destDev, srcDev, com, timestamp, queuePk)
    print("New timestamp: ", packet, " length :", len(packet))

    # String: XX-XX-XX-XX-17-XX-XX-XX-XX-XX-XX-XX-XX-XX-00-01-XX-XX
    # Destination Device: XX-XX // destination device
    # Source Device: XX-XX // source device
    # Command: 17 // muscle results
    # Actual timestamp: XX-XX-XX-XX-XX-XX-XX-XX
    # Payload Bytes: 00-00-00-04
    # Force Value: XX-XX-XX-XX
    # Number of bytes: 21
    com = mc.cMuscleRes
    timestamp = struct.pack(">Q", 11)
    force = struct.pack(">f", 1.0)
    queuePk.append(force)
    del force
    packet = mc.prepareHexPacket(destDev, srcDev, com, timestamp, queuePk)
    print("Force results: ", packet, " length :", len(packet))

    # String: XX-XX-XX-XX-0F-XX-XX-XX-XX-XX-XX-XX-XX-00-00-00-00
    # Destination Device: XX-XX // destination device
    # Source Device: XX-XX // source device
    # Command: 0F // reset simulation
    # Timestamp: XX-XX-XX-XX-XX-XX-XX-XX
    # Payload Bytes: 00-00-00-00
    # Number of bytes: 17
    com = mc.cReset
    timestamp = struct.pack(">Q", 11)
    force = struct.pack(">f", 1.0)
    packet = mc.prepareHexPacket(destDev, srcDev, com, timestamp, queuePk)
    print("Reset: ", packet, " length :", len(packet))

    # String: 00-00-XX-XX-00-00-00-00-00-00-00-00-00-19-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX-XX
    # Destination Device: 00-00 // broadcast
    # Source Device: XX-XX // source device
    # Command: 0E // initialize simulation parameters
    # Timestamp: 00-00-00-00-00-00-00-00
    # Payload Bytes: 00-00-00-19
    # Time step size: XX-XX-XX-XX
    # Number of cycles: XX-XX-XX-XX-XX-XX-XX-XX
    # Simulation ID: XX-XX-XX-XX-XX-XX-XX-XX
    # Timeout Period: XX-XX // in ms
    # Number of neurons: XX-XX // 0..302
    # Number of muscles: XX // 0 to 135
    # Number of bytes: 42
    com = mc.cConfSim
    timestamp = struct.pack(">Q", 0)
    payload=struct.pack(">L", 25)
    aux=b""
    aux += struct.pack(">L", 1)
    aux+= struct.pack(">Q", 1000)
    aux+= struct.pack(">Q", 1)
    aux+= struct.pack(">H", 1)
    aux += struct.pack(">H", 302)
    aux += struct.pack(">B", 1)
    packet = destDev+srcDev+ com+ timestamp+aux
    print("Reset: ", packet, " length :", len(packet))
