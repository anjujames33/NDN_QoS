// Run tests (from ns-3 folder)

// 1. create optimized build and run simulation scenario.
./waf configure -d optimized --enable-examples
./waf --run=ndn-case1

// 2. Analyze results - Creates output file named lat-<tracefile> 
python  preproc-cases-ndn.py <tracefile>

// 3. Get loss data - Creates file named Loss-lat-<tracefile>
python LossStats.py lat-<tracefile>

// 4. Simulation automation (copy scripts and python files to ns-3 folder)
    a. runtest.sh           // run the simulation. edit scenario file name.
    a. process.sh    // process the result to get loss rate. edit the file name to process.

// 5. Commands to execute script
nohup bash runtest.sh &         // Use nohup and '&' to continue execution in background even if terminal is closed.
nohup bash process.sh &

