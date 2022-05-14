# Distributed-Distance-Vector-Protocol-
This is my repository that contains the implementation of my thesis: 

            "Implementing Optimal Routing Protocols on Programmable Hardware"

I am using a library the Research group in Computer Networks at ETH Zürich (p4utils):
    https://github.com/nsg-ethz/p4-utils

To run the code you must install all dependencies first. You can find it in https://nsg-ethz.github.io/p4-utils/installation.html#

Testing:
  
  run:  python network.py                         -> starts the network and the controllers in background
  run:  python sendComputations.py                -> sends probes to the SWs to start the convergement process of the network

You can also delete the lines in network.py script that execute the controllers in background and run them on a terminal for debugging running the command:
            controller.py s1   (this starts the switch s1)
