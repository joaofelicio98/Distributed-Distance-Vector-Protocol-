#!/usr/bin/env python
import argparse
import sys
import socket
import random
import struct

from scapy.all import *

class CPU_header(Packet):
    name = 'CPU'
    fields_desc = [IPField('dst_addr','127.0.0.1'), BitField('distance',0,16),
                   BitField('seq_no',0,32), BitField('ingress_port',0,16)]

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

    if len(sys.argv)<4:
        print ('pass 2 arguments: <destination> "<distance> <seq_no>"')
        exit(1)

    addr = socket.gethostbyname(str(sys.argv[1]))
    iface = get_if()

    my_header = CPU_header(dst_addr = str(sys.argv[1]), distance = int(sys.argv[2]), seq_no = int(sys.argv[3]), ingress_port=1)

    my_header.show2()
    print

    print ("sending on interface %s to %s" % (iface, str(addr)))
    pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
    pkt = pkt /IP(proto=253) / my_header
    pkt.show2()
    sendp(pkt, iface=iface, verbose=False)


if __name__ == '__main__':
    main()
