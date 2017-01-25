import threadsDef as td
import struct
import id

if __name__ == "__main__":
    config_flag=[False, False, False, False, False, False, False, False]
    simulationid=struct.pack(">Q",1)
    simtimestepsz=struct.pack(">l",1)
    cyclesnum=struct.pack(">Q",1000)
    timeout=struct.pack(">H",1)
    nm=id.nid[0]
    neuron=td.modelController(simulationid,nm,simtimestepsz,cyclesnum,timeout)
    conf_flag=True
    if conf_flag:
        payload = 38
        # Select the initial 11 synaptic inputs
        byte=b""
        for i in range(payload, 2, -1):
            byte += struct.pack(">B", 0)
        word = b"0000011111111111"
        word = struct.pack(">H", int(word, 2))
        byte+=word
        if neuron.set_net(nm,byte):
            print("The net topology was set with success!")
            config_flag[0]=True
        else:
            print("Failed to add net topology!")
        payload = 40
        # Select the initial 11 synaptic inputs
        byte = b""
        for i in range(payload, 0, -1):
            byte += struct.pack(">B", 0)
        if neuron.set_mapsbs(nm,byte):
            print("The map synaptic boards was set with success!")
            config_flag[1] = True
        else:
            print("Failed to map the synaptic boards!")
        model = 1
        model = struct.pack(">B", model)
        timestepsize = 0.05
        timestepsize = struct.pack(">f", timestepsize)
        if neuron.set_nm(nm,model,timestepsize):
            print("Neuron/muscle parameters add with success!")
            tmp = neuron.ls_nm(nm)
            print(tmp)
        else:
            print("Failed to add net topology!")

        wght = []
        for i in range(0, 11, 1):
            lsb = i * 32
            msb = lsb + 31
            lsbc = struct.pack(">H", lsb)
            msbc = struct.pack(">H", msb)
            weight = 1.0
            weight = struct.pack(">f", weight)
            itemId=struct.pack(">H",i)
            itemType=struct.pack(">B",1)
            itemDataType=struct.pack(">B",16)
            itemIntPart=struct.pack(">B",0)
            inLSB=lsbc
            inMSB=msbc
            outLSB=struct.pack(">H", 0)
            outMSB=struct.pack(">H", 0)
            value=weight
            if neuron.set_pv(nm,[itemId, itemType, itemDataType, itemIntPart, inLSB, inMSB, outLSB, outMSB, value]):# [itemId, itemType, itemDataType, itemIntegerPart, inLSB, inMSB, outLSB, outMSB, value]
                print("Parameter or variable added with success!")
            else:
                print("Failed to add parameter or variable")

        i += 1
        lsb = i * 32
        msb = lsb + 31
        lsbc = struct.pack(">H", lsb)
        msbc = struct.pack(">H", msb)
        theta3 = 3.0
        theta3 = struct.pack(">f", theta3)
        itemId = struct.pack(">H", i)
        itemType = struct.pack(">B", 1)
        itemDataType = struct.pack(">B", 16)
        itemIntPart = struct.pack(">B", 0)
        inLSB = lsbc
        inMSB = msbc
        outLSB = struct.pack(">H", 0)
        outMSB = struct.pack(">H", 0)
        value = theta3
        if neuron.set_pv(nm, [itemId, itemType, itemDataType, itemIntPart, inLSB, inMSB, outLSB, outMSB,
                              value]):  # [itemId, itemType, itemDataType, itemIntegerPart, inLSB, inMSB, outLSB, outMSB, value]
            print("Parameter or variable added with success!")
        else:
            print("Failed to add parameter or variable")

        i += 1
        lsb = i * 32
        msb = lsb + 31
        lsbc = struct.pack(">H", lsb)
        msbc = struct.pack(">H", msb)
        theta0 = 5.0
        theta0 = struct.pack(">f", theta0)
        itemId = struct.pack(">H", i)
        itemType = struct.pack(">B", 1)
        itemDataType = struct.pack(">B", 16)
        itemIntPart = struct.pack(">B", 0)
        inLSB = lsbc
        inMSB = msbc
        outLSB = struct.pack(">H", 0)
        outMSB = struct.pack(">H", 0)
        value = theta0
        if neuron.set_pv(nm, [itemId, itemType, itemDataType, itemIntPart, inLSB, inMSB, outLSB, outMSB,
                              value]):  # [itemId, itemType, itemDataType, itemIntegerPart, inLSB, inMSB, outLSB, outMSB, value]
            print("Parameter or variable added with success!")
        else:
            print("Failed to add parameter or variable")

        i += 1
        lsb = i * 32
        msb = lsb + 31
        lsbc = struct.pack(">H", lsb)
        msbc = struct.pack(">H", msb)
        theta1 = -0.033333333333
        theta1 = struct.pack(">f", theta1)
        itemId = struct.pack(">H", i)
        itemType = struct.pack(">B", 1)
        itemDataType = struct.pack(">B", 16)
        itemIntPart = struct.pack(">B", 0)
        inLSB = lsbc
        inMSB = msbc
        outLSB = struct.pack(">H", 0)
        outMSB = struct.pack(">H", 0)
        value = theta1
        if neuron.set_pv(nm, [itemId, itemType, itemDataType, itemIntPart, inLSB, inMSB, outLSB, outMSB,
                              value]):  # [itemId, itemType, itemDataType, itemIntegerPart, inLSB, inMSB, outLSB, outMSB, value]
            print("Parameter or variable added with success!")
        else:
            print("Failed to add parameter or variable")

        i += 1
        lsb = i * 32
        msb = lsb + 31
        lsbc = struct.pack(">H", lsb)
        msbc = struct.pack(">H", msb)
        theta2 = 0.8333333333333
        theta2 = struct.pack(">f", theta2)
        itemId = struct.pack(">H", i)
        itemType = struct.pack(">B", 1)
        itemDataType = struct.pack(">B", 16)
        itemIntPart = struct.pack(">B", 0)
        inLSB = lsbc
        inMSB = msbc
        outLSB = struct.pack(">H", 0)
        outMSB = struct.pack(">H", 0)
        value = theta2
        if neuron.set_pv(nm, [itemId, itemType, itemDataType, itemIntPart, inLSB, inMSB, outLSB, outMSB,
                              value]):  # [itemId, itemType, itemDataType, itemIntegerPart, inLSB, inMSB, outLSB, outMSB, value]
            print("Parameter or variable added with success!")
        else:
            print("Failed to add parameter or variable")

        i += 1
        lsb = i * 32
        msb = lsb + 31
        lsbc = struct.pack(">H", lsb)
        msbc = struct.pack(">H", msb)
        force = 0.0
        force = struct.pack(">f", force)
        itemId = struct.pack(">H", i)
        itemType = struct.pack(">B", 1)
        itemDataType = struct.pack(">B", 16)
        itemIntPart = struct.pack(">B", 0)
        inLSB = lsbc
        inMSB = msbc
        outLSB = struct.pack(">H", 0)
        outMSB = struct.pack(">H", 0)
        value = force
        if neuron.set_pv(nm, [itemId, itemType, itemDataType, itemIntPart, inLSB, inMSB, outLSB, outMSB,
                              value]):  # [itemId, itemType, itemDataType, itemIntegerPart, inLSB, inMSB, outLSB, outMSB, value]
            print("Parameter or variable added with success!")
        else:
            print("Failed to add parameter or variable")
        config_flag[2] = True
        print(config_flag)

        # test rtw
        # [startTmstp, endTmstp, SamplingPeriod,[Var1 ... Varn]]
        startTmstp=struct.pack(">Q",10)
        endTmstp=struct.pack(">Q",20)
        sampPeriod=struct.pack("B",1)
        var=[struct.pack(">H",1), struct.pack(">H",2), struct.pack(">H",3)]
        if struct.unpack(">Q",startTmstp)[0]<struct.unpack(">Q",endTmstp)[0]:
            if neuron.set_rtw(nm,[startTmstp,endTmstp,sampPeriod,var[0],var[1], var[2]]):
                print("rtw added with success!")
            else:
                print("Failed to set rtw")
        else:
            print("Error: The start timestamp mus be bigger than the end timestamp")

        # test pcs
        # [startTmstp, endTmstp, value A, Value B, Value C]
        startTmstp = struct.pack(">Q", 10)
        endTmstp = struct.pack(">Q", 20)
        valuea= struct.pack(">f",1)
        valueb = struct.pack(">f", 2)
        valuec = struct.pack(">f", 3)
        if neuron.set_pcs(nm, [startTmstp, endTmstp, valuea, valuec]):
            print("PCS added with success!")
        else:
            print("Failed to add PCS.")

        # test rtw results
        # [itemid, timestamp, value]
        for i in range(0,20,1):
            itemId = struct.pack(">H", 1)
            timestamp = struct.pack(">Q", i)
            value =  struct.pack(">f", i)
            if neuron.push_rtwresults(nm, [itemId, timestamp, value]):
                print("RTW result added with success!")
                print(neuron.ls_size_rtwresults(nm))
                print(neuron.pop_rtwresuts(nm))
            else:
                print("Failed to add RTW result.")

        # test sf results
        # [timetamp, spikes/forces]
        for i in range(0, 20, 1):
            timestamp = struct.pack(">Q", i)
            value = struct.pack(">B", 1)
            if neuron.push_sfresults(nm, [timestamp, value]):
                print("SF result added with success!")
                print(neuron.ls_size_sfresults(nm))
                print(neuron.pop_sfresuts(nm))
            else:
                print("Failed to add SF result.")


        tmp1 = neuron.ls_size_pv(nm)
        for j in range(0,tmp1,1):
            print(neuron.get_pv(nm,j))
        tmp2 = neuron.ls_nm(nm)
        tmp3= neuron.ls_rtw(nm)
        tmp4= neuron.ls_pcs(nm)
        print("Number of Parameters/Variables: ", tmp1)
        print("List neuron/muscles details: ",tmp2)
        print("RTW: ",tmp3)
        print("PCS: ",tmp4)


        del neuron
    else:
        print("Error. The object does not exists!")