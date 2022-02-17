#!/usr/bin/env python
import argparse
import sys
import socket
import random
import struct
from p4utils.utils.helper import load_topo
from scapy.all import *

class CPU_header(Packet):
    name = 'CPU'
    fields_desc = [BitField('ingress_port', 0, 16)]

def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print ("Cannot find eth0 interface")
        exit(1)
    return iface

def main():

    if len(sys.argv)<6:
        print ('pass 4 arguments: <destination> <distance> <seq_no> <port> <sw_name>')
        exit(1)

    sw_name = sys.argv[5]
    topo = load_topo('topology.json')
    cpu_port_intf = str(topo.get_cpu_port_intf(sw_name))

    addr = socket.gethostbyname(str(sys.argv[1]))
    iface = get_if()

    my_header = CPU_header(ingress_port=int(sys.argv[4]))
    bind_layers(IP, CPU_header, proto = 253)

    data = "destination=" + str(sys.argv[1])
    data = data + " | distance=" + str(sys.argv[2])
    data = data + " | seq_no=" + str(sys.argv[3])

    print ("sending on interface %s for dst %s" % (iface, str(addr)))
    pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
    pkt = pkt / IP(src=sys.argv[1], proto=253) / my_header / data
    pkt.show2()
    sendp(pkt, iface=iface, verbose=False)


if __name__ == '__main__':
    main()
