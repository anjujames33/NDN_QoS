'''
Created on Jul 25, 2020

@author: Anju
'''

import socket
import json

SimulationStarttime = 0   
SimulationEndtime = 11#8640  # 6*60*24
    
# Create socket client
HOST, PORT = "192.168.43.135", 5005
CHUNK_SIZE = 750  # for a safe side use 900 instead of 1024
PACKET_SIZE = 1023  # for a safe side use 900 instead of 1024
clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsock.connect((HOST, PORT))
print('..... connection established .....')
client_name = "ReDisPV"

clientsock.send(client_name.encode())
data = clientsock.recv(PACKET_SIZE).decode()


# Run the simulation
for t in range(SimulationStarttime, SimulationEndtime):
    print(t)    # Print time step
   
    # Read data from 'redispv2comlayer_0.json' and send to ndnSIM as chunks  
    with open('redispv2comlayer_0.json') as f:
        data_to_com = json.load(f)        
        
    data_to_com_str = json.dumps(data_to_com)    
    #print(data_to_com_str)
    message_dictionary = {}
    
    # Split measurement json into chunks of size 'CHUNK_SIZE'
    chunks = [data_to_com_str[i:i + CHUNK_SIZE] for i in range(0, len(data_to_com_str), CHUNK_SIZE)]    
    n = len(chunks)
    message_dictionary['size'] = len(data_to_com_str)  # set first key in message_dictionary dictionary - total size of one time step data
    
    # Send data as json dictionary with chunks.
    i = 0    
    while i < n:
        
        # Set flag to identify end of one time step data.
        if i < n - 1:
            finished = 0
        else:
            finished = 1
         
        # Fill dictionary    
        message_dictionary['payload'] = chunks[i]
        message_dictionary['finished'] = finished
        message_dictionary['payloadsize'] = len(chunks[i])
        message_dictionary['0'] = ""
        
        packet_json = json.dumps(message_dictionary)
        
        # Fill message_dictionary with 0s to make it PACKET_SIZE size.
        zeros = PACKET_SIZE - len(packet_json)
        for z in range(0, zeros):
            message_dictionary["0"] = message_dictionary["0"] + "0"
            
        packet_json = json.dumps(message_dictionary)
        print(packet_json)
        i += 1
        
        # Send encoded data
        clientsock.send(packet_json.encode())
    
        
    # Receive data as chunks
    done = False
    file = ""
    
    while not done: 
        
        data = clientsock.recv(1023).decode()
        ret = len(data)
        size = 0
        rec = 0
        
        if ret > 0:
            print("Size of Read " + str(ret))
            print("Payload:    " + data)
            
            #while ret < 1023:
            pdata = clientsock.recv(1023 - (ret)).decode()
            data = data + pdata
            ret = len(data)
            print("Building... " + str(ret))
         
            tempj = json.loads(data)
            size = tempj["size"]
            
            if tempj["finished"] == 1:
                done = True
                
            file += tempj["payload"]
            temp = int(tempj["payloadsize"])
            rec = rec + temp;

    print("====" + file)    


clientsock.close()
print('..... connection closed .....')        
        
 