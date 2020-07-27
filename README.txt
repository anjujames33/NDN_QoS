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

5.Run QoS application
---------------------
cd ns-3
NS_LOG=ndn.Consumer:ndn.Producer ./waf --run=ndn-qos



II. Folder Structure
=====================
1. ns-3 			- Code base
2. process_result	- Python scripts for Monte Carlo simulations and result processing
3. thirdparty		- Thirdparty libraries used (Required to build the code without error)
4. topology			- Topology files for Monte Carlo simulations used in scenario files
5. clients			- Python clients to connect from windows machine to test 123-bus system.
