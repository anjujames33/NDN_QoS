#!/bin/bash

max=20
for (( i=1; i <= $max; ++i ))
do
	python preproc-cases-ndn.py ndn-case1-run$i.csv
    python LossStats.py lat-ndn-case1-run$i.csv
    echo "Finished instance $i at $(date)!"
done
