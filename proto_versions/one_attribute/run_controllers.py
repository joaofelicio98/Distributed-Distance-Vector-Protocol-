#from controller import ControllerThread
from p4utils.utils.helper import load_topo
import threading

topo = load_topo('topology.json')

def main():
    #nodes = topo.get_nodes(fields=['isSwitch'])
    #for node in list(nodes):
    #    if node == 'sw-cpu' or not nodes[node]:
    #        del nodes[node]

    #print (topo.get_host_ip('h1'))

    interfaces_to_port = topo.get_node_intfs(fields=['port'])['s1'].copy()
    print(interfaces_to_port)
    for intf in interfaces_to_port:
        if interfaces_to_port[intf] == 1:
            print(intf)

if __name__ == "__main__":
    main()
