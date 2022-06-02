#!/usr/bin/env python2
import argparse
import grpc
import os
import sys
import ctypes
from time import sleep
from scapy.all import *
import threading
import nnpy

from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI

CPU_HEADER_PROTO = 253
MY_HEADER_PROTO = 254

class CPU_header(Packet):
    name = 'CPU'
    fields_desc = [IPField('destination', '127.0.0.1'),
                    BitField('next_hop',0,15), BitField('new_destination',0,1),
                    BitField('info',0,32), BitField('test',0,8)]

class Controller():

    def __init__(self, sw_name):
        self.topo = load_topo('topology.json')
        self.sw_name = sw_name
        self.cpu_port = self.topo.get_cpu_port_index(self.sw_name)
        device_id = self.topo.get_p4switch_id(sw_name)
        grpc_port = self.topo.get_grpc_port(sw_name)
        sw_data = self.topo.get_p4rtswitches()[sw_name]
        self.controller = SimpleSwitchP4RuntimeAPI(device_id, grpc_port,
                                                   p4rt_path=sw_data['p4rt_path'],
                                                   json_path=sw_data['json_path'])

        # To count the number of changing of states
        self.count_states=0
        # Indexes to get the count values and elected's next hop
        self.info = {}
        self.init()


    def reset(self):
        # Reset grpc server
        self.controller.reset_state()
        # Due to a bug in the way the grpc switch reset its states with the message
        # SetForwardingPipelineConfigRequest and Action VERIFY_AND_COMMIT (this is
        # a problem in the implementation of the server), subsequent initializations
        # (i.e. those which happen after the switch reset) of multicast groups
        # (with the same multicast id) are appended to the previous ones
        # (i.e. those present before the reset), which are supposed to be erased by the reset, but
        # they actually are not. This leads to duplicate packets sent to the same port.
        # This seems to be caused by the fact that, even if the grpc server is reset, the
        # switch forwarding states are not completely erased. In order to overcome this,
        # a complete reset can be achieved by resetting the switch via thrift.
        thrift_port = self.topo.get_thrift_port(self.sw_name)
        controller_thrift = SimpleSwitchThriftAPI(thrift_port)
        # Reset forwarding states
        controller_thrift.reset_state()

    def init(self):
        self.reset()
        self.add_broadcast_groups()
        self.add_initial_ipv4_rules()
        self.add_clone_session()
        self.add_cpu_rule()


    def add_broadcast_groups(self):
        print("==========================================")
        print()
        print("Creating the multicast groups...")
        interfaces_to_port = self.topo.get_node_intfs(fields=['port'])[self.sw_name].copy()
        # Filter lo, cpu port and port to hosts
        interfaces_to_port.pop('lo', None)
        interfaces_to_port.pop(self.topo.get_cpu_port_intf(self.sw_name), None)
        intf_to_pop = []
        hosts_ports = []
        # Remove all ports that connect to hosts
        for intf, ingress_port in interfaces_to_port.items():
            node_name = self.topo.port_to_node(self.sw_name, ingress_port)
            if node_name in self.topo.get_hosts():
                intf_to_pop.append(intf)
                hosts_ports.append(ingress_port)
        for intf in intf_to_pop:
            interfaces_to_port.pop(intf, None)

        #for port in hosts_ports:
            # Add multicast group and ports
        #    self.controller.mc_mgrp_create(port, list(interfaces_to_port.values()))
            # Fill broadcast table
        #    self.controller.table_add("broadcast_elected_attr", "set_mcast_grp", [str(port)], [str(port)])

        for ingress_port in interfaces_to_port.values():
            port_list = list(interfaces_to_port.values())
            del(port_list[port_list.index(ingress_port)])

            # Add multicast group and ports
            self.controller.mc_mgrp_create(ingress_port, port_list)
            # Fill broadcast table
            #print ("DEBUG: creating mcastgrp: {} for ports: {}".format(ingress_port, port_list))
            self.controller.table_add("broadcast_elected_attr", "set_mcast_grp", [str(ingress_port)], [str(ingress_port)])

        self.controller.mc_mgrp_create(self.cpu_port, list(interfaces_to_port.values()))
        print(f"BROADCAST: {interfaces_to_port.values()}")
        self.controller.table_add("broadcast_elected_attr", "set_mcast_grp", [str(self.cpu_port)], [str(self.cpu_port)])

    #IPv4 rules for every host connected to the switch
    def add_initial_ipv4_rules(self):
        print("==========================================")
        print()
        print("Adding the initial ipv4 rules...")
        self.controller.table_set_default("check_destination_known", "elect_new_destination")
        neighbors = self.topo.get_neighbors(self.sw_name)

        for node in neighbors:
            if self.topo.isHost(node):
                #dst_ip = self.topo.get_host_ip(node)
                dst_mac = self.topo.node_to_node_mac(node, self.sw_name)
                port = self.topo.node_to_node_port_num(self.sw_name, node)
                subnet = self.topo.subnet(node, self.sw_name)
                self.controller.table_add("ipv4_lpm", "ipv4_forward", [subnet], [dst_mac, str(port)])
                self.controller.table_add("check_destination_known", "get_info", [subnet],
                                            [str(port), str(0)])
                self.info[subnet] = {}
                self.info[subnet]["NH"] = port

    def add_clone_session(self):
        print("==========================================")
        print()
        print("Adding the clone session...")
        if self.cpu_port:
            self.controller.cs_create(100, [self.cpu_port])


    def add_cpu_rule(self):
        print("==========================================")
        print()
        print("Adding CPU rule...")
        if self.cpu_port:
            self.controller.table_add("cpu_table", "send_to_cpu", [str(MY_HEADER_PROTO)], [str(self.cpu_port)])

    # Main loop
    def run(self):
        try:
            while True:
                cpu_port_intf = str(self.topo.get_cpu_port_intf(self.sw_name))
                print("==========================================")
                print()
                print(f"DEBUG: {self.sw_name} | sniffing at port: {cpu_port_intf}")
                sniff(iface=cpu_port_intf, prn=self.recv_msg_cpu)
        except KeyboardInterrupt:
            print(f"Ending controller {self.sw_name}")
            self.reset()

    def get_subnet(self, dst_ip):
        host = self.topo.get_host_name(dst_ip)
        node = self.topo.get_neighbors(host)[0]

        subnet = self.topo.subnet(host, node)
        return subnet

    def recv_msg_cpu(self, pkt):
        #print('DEBUG: {} | Received a new packet!'.format(self.sw_name))
        #print(pkt[IP].proto)
        if pkt[IP].proto == CPU_HEADER_PROTO:
            #print()
            #pkt.show2()
            #print()
            pkt = Ether(raw(pkt))
            cpu_header = CPU_header(bytes(pkt.load))
            dst_ip = cpu_header.destination
            subnet = self.get_subnet(dst_ip)
            port = cpu_header.next_hop
            is_new = cpu_header.new_destination
            index = cpu_header.info
            test = cpu_header.test

            print(f"DEBUG {self.sw_name} | destination = {subnet}")
            print(f"DEBUG {self.sw_name} | next hop = {port}")
            print(f"DEBUG {self.sw_name} | is_new = {is_new}")
            print(f"DEBUG {self.sw_name} | index = {index}")
            print(f"DEBUG {self.sw_name} | test = {test}")
            print()

            if not port == self.cpu_port:
                print(f"DEBUG: {self.sw_name} | Received a new attribute to elect!")
                self.count_states += 1
                print(f"DEBUG {self.sw_name} changed its state {self.count_states} times.")

            if port == self.cpu_port:
                self.info[subnet]["index"] = index
            elif is_new == 1:
                self.info[subnet] = {}
                self.info[subnet]["index"] = index
                self.info[subnet]["NH"] = port
                count = self.controller.counter_read("packet_counter", self.info[subnet]["index"])
                self.add_new_entry(subnet, port, count)
                self.send_back_to_switch(pkt, dst_ip, count)
            else:
                self.info[subnet]["NH"] = port
                count = self.controller.counter_read("packet_counter", self.info[subnet]["index"])
                self.modify_entry(subnet, port, count)
                self.send_back_to_switch(pkt, dst_ip, count)
            print()
            print("==========================================")
            print()

    def add_new_entry(self, dst_ip, port, count):
        print("==========================================")
        print()
        print("Adding a new entry to the ipv4_lpm table...")
        print()
        print(f"COUNTER = {count[1]}")
        print()

        neighbor = self.topo.port_to_node(self.sw_name, port)
        dst_mac = self.topo.node_to_node_mac(self.sw_name, neighbor)
        self.controller.table_add("ipv4_lpm", "ipv4_forward",
                                [str(dst_ip)], [dst_mac, str(port)])
        self.controller.table_add("check_destination_known", "get_info", [str(dst_ip)],
                                    [str(self.info[dst_ip]["NH"]), str(count[1])])

    def modify_entry(self, dst_ip, port, count):
        print("==========================================")
        print()
        print("Modifying an entry in the ipv4_lpm table...")
        print()
        print(f"COUNTER = {count[1]}")
        print()

        neighbor = self.topo.port_to_node(self.sw_name, port)
        dst_mac = self.topo.node_to_node_mac(self.sw_name, neighbor)
        self.controller.table_modify_match("ipv4_lpm", "ipv4_forward",
                                [str(dst_ip)], [dst_mac, str(port)])
        self.controller.table_modify_match("check_destination_known", "get_info", [str(dst_ip)],
                                    [str(self.info[dst_ip]["NH"]), str(count[1])])

    def get_if(self, sw):
        hosts = self.topo.get_hosts_connected_to(sw)
        interfaces = self.topo.get_node_intfs(fields=['port'])[sw].copy()
        iface = ""
        for intf, port in interfaces.items():
            if hosts[0] in intf:
                iface = intf
                break

        return iface


    def send_back_to_switch(self, pkt, dst_ip, count):
        cpu_header = CPU_header(destination = dst_ip, info = count)
        pkt[IP].remove_payload()
        pkt = pkt / cpu_header

#        pkt.show2()
        iface = self.get_if(self.sw_name)
        sendp(pkt, iface=iface, verbose=False)

if __name__ == "__main__":
    import sys
    sw_name = sys.argv[1]
    controller = Controller(sw_name).run()
