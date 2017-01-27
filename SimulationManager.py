# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 18:17:32 2016

@author: pedromachado
"""

import threading
import time
from http.server import HTTPServer
import threadsDef as td
import downloadManager as dm
import socketserver
import socket

PORT = 3000
PORT1 = 9000
PORT2 = 4000
serverIP=""


if __name__ == "__main__":
    initialTime=time.strftime("%d/%m/%Y %H:%M:%S")
    td.flag=True
    jobs=[]
    servers=[]
    string=[]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    IP=s.getsockname()[0]
    #for i in range(1,330,1): # comment this line
        # IP="100.100."
        # if i<256:
        #     IP+="0."+str(i)
        # else:
        #     IP+="1."+str(i-256)
    ip0=int(IP[8:9])
    ip1 = int(IP[10:len(IP)])
    if ip0==1 and 46<ip1<74:
        type="Muscle # "+str(((ip1+ip0*256)-302))
    elif ip0==1 and ip1<47:
        type="Neuron # "+str(ip1+ip0*256)
    elif ip0==0:
        type = "Neuron # " + str(ip1)
    else:
        type="Other Device"
    server = socketserver.TCPServer((serverIP, PORT), dm.MyTCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    servers.append(server)
    jobs.append(server_thread)
    stri=("Interface Manager TCP messages. Serving endpoint: "+str(IP)+":"+str(PORT))
    string.append(stri)

    server = socketserver.UDPServer(('', PORT2), dm.MyUDPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    servers.append(server)
    jobs.append(server_thread)
    stri = ("Interface Manager UDP messages. Serving endpoint : " + str(IP) + ":" + str(PORT2))
    string.append(stri)

    server = HTTPServer((serverIP, PORT1), dm.HTTPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    servers.append(server)
    jobs.append(server_thread)
    stri = ("Ethernet Blaster service. Serving endpoint: " + str(IP) + ":" + str(PORT1))
    string.append(stri)
    RUS = threading.Thread(target=td.RUS, args=(td.qRUSi,td.qRUSo))
    RUS.setDaemon(True)
    jobs.append(RUS)
    stri=("Starting the RUS service...")
    td.qRUSi.put(["start"])
    string.append(stri)
    IM = threading.Thread(target=td.IM, args=(td.qIMi,td.qIMo,))
    IM.setDaemon(True)
    jobs.append(IM)
    stri=("Starting the IM service...")
    td.qIMi.put(["start"])
    string.append(stri)
    MC = threading.Thread(target=td.MC, args=(td.qi,td.qo,))
    MC.setDaemon(True)
    jobs.append(MC)
    stri=("Starting the Model Controller service...")
    td.qi.put(["start"])
    string.append(stri)
    
    
    
    i=0
    log="***********************Starting "+type+" controller **************************"
    print(log)
    for j in jobs:
        log=j.getName()+", "+string[i]
        print(log)
        j.start()
        i+=1
    del string
    time.sleep(0.01)
    log="\n\nThe " + type + " is online since: "+initialTime
    print(log)
    log=type+" - version: "+str(td.MCversion)
    print(log)
    try:
        while td.flag:
            time.sleep(0.1)
    except KeyboardInterrupt:
        td.flag=False
        for s in servers:
            s.shutdown()
            s.server_close()
        log='All the servers were closed with success.'
        print(log)
        #Closing
        td.qi.put(["close"])
        td.qi.join()
        log=td.qo.get()
        td.qo.task_done()
        td.qo.join()
        print(log)

        #Closing RUS
        td.qRUSi.put(["close"])
        td.qRUSi.join()
        log=td.qRUSo.get()
        td.qRUSo.task_done()
        td.qRUSo.join()
        print(log)

        #Closing IM
        td.qIMi.put(["close"])
        td.qIMi.join()
        log=td.qIMo.get()
        td.qIMo.task_done()
        td.qIMo.join()
        print(log)

        time.sleep(0.001)
        log="Deleting queues..."
        print(log)
        del td.qo
        del td.qi
        del td.qRUSi
        del td.qRUSo
        del td.qIMi
        del td.qIMo
        MC.join()
        RUS.join()
        IM.join()
        for j in jobs:
            if j.isAlive()==False:
                log=j.getName()+" was closed with success!"
                print(log)
            else:
                log=j.getName()+" is still in memory!"
                print(log)
        log="MC software closed at: "+time.strftime("%d/%m/%Y %H:%M:%S")
        print(log)
        log="++++++++++++++++"+type+" controller closed!++++++++++++++++++++++++++++++"
        print(log)        
    
