'''
Created on May 21, 2020

@author: spate181
'''
from opendss_sim import opendsstools

import socket
import json

# Change file location based on 650 or 123
dssfilelocation = 'C:\\Users\\Anju\\eclipse-workspace\\Simulator123bus\\IEEE123bus_withPV\\'  
ig = opendsstools(dssfilelocation + "Master.dss")
list_of_sensors = 'C:\\Users\\Anju\\eclipse-workspace\\Simulator123bus\\IEEE123bus_withPV\\sensor_location.csv'
ig.initialize_log(list_of_sensors)
SimulationStarttime = 0   
SimulationEndtime = 11  # 8640  # 6*60*24
    
ig.setuppowerflow(0)
ig.loadscaling()  # loading feeder load profiles

# Create socket client
# HOST, PORT = "172.24.18.115", 5005
HOST, PORT = "192.168.43.135", 5005
CHUNK_SIZE = 750  # for a safe side use 900 instead of 1024
PACKET_SIZE = 1023  # for a safe side use 900 instead of 1024
clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsock.connect((HOST, PORT))
print('..... connection established .....')
client_name = "OpenDSS"
clientsock.send(client_name.encode())
data = clientsock.recv(PACKET_SIZE).decode()

# Run the simulation
for t in range(SimulationStarttime, SimulationEndtime):
    print(t)  # Print time step
    ig.powerflow(t)
    [sim_time, measurements] = ig.log_measurements()
    data_to_com_str = json.dumps(measurements)    
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
        i += 1
        
        # Send encoded data
        clientsock.send(packet_json.encode())
    
    
    #==================================================================================   
    # Receive Lead DER data from ReDis-PV
    more = True
    data = clientsock.recv(1023).decode()
    leads = int(data)
    print(leads)
    
    # Read data until all leads are read
    while leads > 0:
        leads -= 1;
        done = False
        
        # Read data from Lead DER until 'finished' flag is set
        while not done:
            data = clientsock.recv(1023).decode()
            ret = len(data)
            size = 0
            rec = 0
            file = ""
            
            if ret > 0:
                print("Size of Read: " + str(ret))
                print("Payload from Lead DER: " + data)
                
                # 
                while ret < 1023:
                    pdata = clientsock.recv(1023 - (ret + 1)).decode()
                    data = data + pdata
                    ret = len(data)
                    print("Building... " + str(ret))
                
                # Create JSON object from received data 
                tempj = json.loads(data)
                size = tempj["size"]
                if tempj["finished"] == 1:
                    done = True
                file += tempj["payload"]
                temp = int(tempj["payloadsize"])
                rec = rec + temp;
        
        # Print file with payloads from LEAD DERs        
        print(file)
        
        # Create JSON dictionary to send to following DERs
        rec_json = json.loads(file)
        follwerSetPoints = {}
        
        for each in rec_json:
            if each != rec_json[each]["Lead_DER"]:
                follwerSetPoints[each] = rec_json[each]
                
        if follwerSetPoints == {}:
            continue
        
        print(json.dumps(follwerSetPoints));
        send_json = json.dumps(follwerSetPoints)
        
        # Send data as chunks to following DERs
        chunks = [send_json[i:i + CHUNK_SIZE] for i in range(0, len(send_json), CHUNK_SIZE)]
        n = len(chunks)
        
        message_dictionary['size'] = len(send_json)  # set first key in message_dictionary dictionary - total size of one timestep data
        i = 0
        
        # Send all data chunks
        while i < n:
            
            if i < n - 1:
                finished = 0
            else:
                finished = 1
                
            message_dictionary['payload'] = chunks[i]
            message_dictionary['finished'] = finished
            message_dictionary['payloadsize'] = len(chunks[i])
            message_dictionary["0"] = ""
            
            pj = json.dumps(message_dictionary)
            zeros = 1023 - len(pj)
            
            for z in range(0, zeros):
                message_dictionary["0"] = message_dictionary["0"] + "0"
                
            pj = json.dumps(message_dictionary)
            i += 1
            clientsock.send(pj.encode())
    
    
    #==================================================================================  
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
            
            # while ret < 1023:
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

# Measurement format:
# simtime: seconds
# For active/reactive power and voltage measurements, Type Array: [PhA, PhB, PhC]
# For Busdata, Type: List, Format=[Name, Distance from subsystem, X coordinate, Y coordinate]
