#!/bin/bash

max=20
for (( i=1; i <= $max; ++i ))
do
    NS_GLOBAL_VALUE="RngRun=$i" ./waf --run="ndn-case1 --Run=$i" 
    echo "Finished instance $i at $(date)!"
done
