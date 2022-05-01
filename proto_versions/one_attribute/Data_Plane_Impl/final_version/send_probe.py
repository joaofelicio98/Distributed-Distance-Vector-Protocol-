#!/usr/bin/env python
import argparse
import sys
import socket
import random
import struct
from p4utils.utils.helper import load_topo
from scapy.all import *

class Probe(Packet):
    name = 'Probe'
    fields_desc = [IPField('destination', '127.0.0.1'),
                    BitField('distance', 0, 16), BitField('seq_no',0,32)]


topo = load_topo('topology.json')

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

def get_intf(sw, port):
    interfaces_to_port = topo.get_node_intfs(fields=['port'])[sw].copy()
    for intf, ingress_port in interfaces_to_port.items():
        if ingress_port == port:
            return intf
    raise AssertionError(f'Port {port} doesnt exist in {sw}.')

def main():

    if len(sys.argv)<6:
        print ('pass 5 arguments: <destination> <distance> <seq_no> <port> <sw_name>')
        exit(1)

    dst = sys.argv[1]
    distance = int(sys.argv[2])
    seq_no = int(sys.argv[3])
    port = int(sys.argv[4])
    sw_name = sys.argv[5]

    intf = get_intf(sw_name, port)

    probe = Probe(destination=dst, distance=distance, seq_no=seq_no)
    bind_layers(IP, Probe, proto = 254)

    print (f"Sending on interface {intf} for destination {dst}")
    pkt =  Ether(src=get_if_hwaddr(intf), dst='ff:ff:ff:ff:ff:ff')
    pkt = pkt / IP(proto=254) / probe
    pkt.show2()
    sendp(pkt, iface=intf, verbose=False)


if __name__ == '__main__':
    main()
