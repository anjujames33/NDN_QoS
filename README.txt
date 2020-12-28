I. NDN_QoS
===========

1. Code Checkout:
----------------
git clone https://github.com/anjujames33/NDN_QoS.git	// Clone ns3 alone OR
git clone -b qos https://github.com/anjujames33/NDN_QoS.git	// To checkout qos branch
cd NDN_QoS/	// Move to NDN_QoS directory
git clone --recursive https://github.com/anjujames33/ndnSIM.git ns-3/src/ndnSIM	// Clone ndnSIM, NFD and ndn-cxx

2. Check branch details (make sure you are in 'qos' branch in NDN_QoS, ndnSIM, NFD and ndn-cxx folders)
-----------------------
git branch -a	// Show all branches and the current branch with * symbol.
git remote -v	// Display git url

3. Build code
-------------
cd ns-3/	// Move to ns-3 directory
./waf configure --enable-examples	// configure with examples
./waf	// build code once

4. Pushing the code
-------------------
git branch -a	// Make sure you are in proper branch(qos) before making modifications.
git checkout <branch_name>	// To checkout to a spacific branch
git status	// In modified git directory(ndnSIM,NFD,ndn-cxx) will show modified or new file in red color
git add .	// Add all modified files to repository or select individual files instead of dot to add that file alone.
git status	// All the files added to git will change color to green. If something is not added, will remain in red color
git commit -m "Add meaningful comment summerizing the modification made"	// Code commiting locally
git push origin qos	// Pushing the code to remote branch

5.Run QoS enabled Simulation
----------------------------
cd ns-3
NS_LOG=ndn.Consumer:ndn.Producer ./waf --run=ndn-qos



II. Folder Structure
=====================
1. ns-3 			- Code base
2. process_result	- Python scripts for simulations and result processing.
3. thirdparty		- Thirdparty libraries used (Required to build the code without error)
4. topology			- Topology files for Monte Carlo simulations used in scenario files
5. clients			- Python clients to connect from windows machine to test 123-bus system.


III. New files (New Mexico State University)
=====================================================

1. ns-3/src/ndnSIM/NFD/daemon/fw

	ndn-priority-tx-queue.cpp
	ndn-priority-tx-queue.hpp
	ndn-qos-queue.cpp
	ndn-qos-queue.hpp
	ndn-token-bucket.cpp
	ndn-token-bucket.hpp
	qos-strategy.cpp
	qos-strategy.hpp
	TBucket.cpp
	TBucket.hpp

2. ns-3/src/ndnSIM/apps

	ConsumedTokens.cpp
	ConsumedTokens.hpp
	ndn-aggregator.cpp
	ndn-aggregator.hpp
	ndn-subscriber.cpp
	ndn-subscriber.hpp
	ndn-subscriber-sync.cpp
	ndn-subscriber-sync.hpp
	ndn-synchronizer.cpp
	ndn-synchronizer.hpp
	ndn-synchronizer-socket.cpp
	ndn-synchronizer-socket.hpp
	parser-OpenDSS.cpp
	parser-OpenDSS.hpp
	parser-ReDisPv.cpp
	parser-ReDisPv.hpp
	token-bucket.cpp
	token-bucket.hpp

IV . Documentation
==================
Documentation is available in ns-3/src/ndnSIM/docs/html/ folder.
Open index.html in browser and you will be able to find the documentation similar to ndnSIM.

