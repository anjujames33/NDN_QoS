from __future__ import division 
import csv 
import sys 
from collections import defaultdict 
import numpy as np 
import matplotlib.pyplot as plt 
import glob

def main(filepath=None, maxSuccess=None):
    count = []
    node_count = 0;
    latency_sum = {}
    latency_count = {};
    lossCount = {};
    tp = []
    sent = []
    nodes = {};
    for i in range(0,35):
	tp.append(0)
	count.append(0)
	sent.append(0)
    if filepath is None and maxSuccess is None:
        sys.stderr.write("usage: python3 %s <file-path> <expected-success-number>\n")
        return 1
    xmax = 250
    cumulatedFullLatencies = []
    filesToProcess = glob.glob(filepath )
    print filesToProcess
    for filename in filesToProcess:
        pending = {}
        pending1 = {}
        fullLatencies = []
        latencies = defaultdict(lambda: [])
        print("Trying :" + filename)
        with open(filename, 'r') as csvh:
            #dialect = csv.Sniffer().sniff(csvh.read(10*1024))
            dialect = csv.Sniffer().has_header(csvh.read(1024))
            csvh.seek(0)
            reader = csv.reader(csvh, delimiter=' ', skipinitialspace=True)
            next(reader) # skip header
            
            for srcid, dstid, timesent, timerecv, latency, flowcls, pktname in reader:
                if flowcls not in latency_count:
                    latency_count[flowcls] = 0
                    lossCount[flowcls] = 0
                latency_count[flowcls] += 1
                print(timerecv)
                if timerecv == "400.000000000":
                   lossCount[flowcls] += 1

 




  


    f = open("Loss-%s"%filepath,"w")
    f.write("flowcls recvcnt recvsize losscnt losssize\n")
    for each in lossCount:
        print latency_count[each];
        f.write(each + "\t" + str(lossCount[each]/latency_count[each]) + " " + str(lossCount[each]*200) + "\n")


    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))

