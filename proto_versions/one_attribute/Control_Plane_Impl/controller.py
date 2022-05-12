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
#from datetime import datetime
import time

from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI

sys.path.append('../Get_stats_API')
from statistics_API import stats_API

CPU_HEADER_PROTO = 253
MY_HEADER_PROTO = 254

class CPU_header(Packet):
    name = 'CPU'
    fields_desc = [BitField('ingress_port', 0, 16)]

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

        #stored elected attributes -> {destination:  [distance,seq_no,port]}
        # destination -> Destination IP into which the attribute is refering to
        # distance -> Distance to reach the destination
        # seq_no -> Sequence Number of the attribute
        # port -> Next port into which the packet will send packets to reach the destination
        self.elected_attr = {}
        #stored promised attributes -> {destination:  [distance,seq_no,port]}
        self.promised_attr = {}

        #probes counter
        self.count_states=0 # To count the number of changing of states
        self.topology = "Test" # Topology I am currently using
        self.Try = 1 # Number of try
        self.stats_api = stats_API(self.Try, self.topology)
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
        self.add_boadcast_groups()
        self.add_initial_ipv4_rules()
        self.add_CPU_rules()
        #self.add_clone_session()


    def add_boadcast_groups(self):
        interfaces_to_port = self.topo.get_node_intfs(fields=['port'])[self.sw_name].copy()
        # Filter lo, cpu port and port to hosts
        interfaces_to_port.pop('lo', None)
        interfaces_to_port.pop(self.topo.get_cpu_port_intf(self.sw_name), None)
        intf_to_pop = []
        for intf, ingress_port in interfaces_to_port.items():
            node_name = self.topo.port_to_node(self.sw_name, ingress_port)
            if node_name in self.topo.get_hosts():
                intf_to_pop.append(intf)
        for intf in intf_to_pop:
            interfaces_to_port.pop(intf, None)

        for ingress_port in interfaces_to_port.values():
            port_list = list(interfaces_to_port.values())
            del(port_list[port_list.index(ingress_port)])

            self.controller.mc_mgrp_create(ingress_port, port_list)

            # Fill broadcast table
            #print ("DEBUG: creating mcastgrp: {} for ports: {}".format(ingress_port, port_list))
            self.controller.table_add("broadcast_elected_attr", "set_mcast_grp", [str(ingress_port)], [str(ingress_port)])

        self.controller.mc_mgrp_create(self.cpu_port, list(interfaces_to_port.values()))
        self.controller.table_add("broadcast_elected_attr", "set_mcast_grp", [str(self.cpu_port)], [str(self.cpu_port)])

    #IPv4 rules for every host connected to the switch
    def add_initial_ipv4_rules(self):
        print("==========================================")
        print()
        print("Adding the initial ipv4 rules...")
        neighbors = self.topo.get_neighbors(self.sw_name)

        for node in neighbors:
            if self.topo.isHost(node):
                #dst_ip = self.topo.get_host_ip(node)
                dst_mac = self.topo.node_to_node_mac(node, self.sw_name)
                port = self.topo.node_to_node_port_num(self.sw_name, node)
                subnet = self.topo.subnet(node, self.sw_name)
                self.controller.table_add("ipv4_lpm", "ipv4_forward", [subnet], [dst_mac, str(port)])

    def add_CPU_rules(self):
        self.controller.table_add("cpu_table", "send_to_cpu", [str(MY_HEADER_PROTO)], [str(self.cpu_port)])

    #def add_clone_session(self):
    #    if self.cpu_port:
    #        self.controller.cs_create(100, [self.cpu_port])


    # Main loop
    def run(self):
        try:
            while True:
                cpu_port_intf = str(self.topo.get_cpu_port_intf(self.sw_name))
                print("==========================================")
                print()
                print(f"DEBUG: {self.sw_name} | sniffing at port: {cpu_port_intf}")
                sniff(iface=cpu_port_intf, prn=self.recv_msg_cpu)
        finally:
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
            print("==========================================")
            print()
            print(f"DEBUG: {self.sw_name} | Received a new attribute!")
            #print()
            #pkt.show2()
            #print()
            pkt = Ether(raw(pkt))
            # Extract ingress port from header
            cpu_header = CPU_header(bytes(pkt.load))
            port = cpu_header.ingress_port
            #port = pkt[CPU_header].ingress_port

            # Extract fields from payload
            data = str(pkt[Padding].load)
            dst = data.rsplit(" | ")[0].rsplit("=")[1]
            subnet = self.get_subnet(dst)
            distance = int(data.rsplit(" | ")[1].rsplit("=")[1])
            seq_no = int(data.rsplit(" | ")[2].rsplit("=")[1][:-1])
            print(f"DEBUG: {self.sw_name} | destination = {subnet} | distance = {distance}| seq_no = {seq_no} | port = {port}")
            params = [subnet, distance, seq_no, port]
            elected = self.make_decision(self.sw_name, params)
            if elected != None:
                self.count_states += 1
                #now = datetime.now()
                #current_time = now.strftime("%H:%M:%S")
                #print("Adding new entry... time = ",current_time)

                current_time = round(time.time()*1000) # get current time in miliseconds
                # Insert new entry to json file
                self.stats_api.insert_new_value(self.sw_name, seq_no, self.count_states, current_time)
                self.announce_attribute(pkt, elected, dst)

    def announce_attribute(self, packet, elected, dst):
        #print(f"DEBUG: {self.sw_name} | announcing an elected attribute for subnet {params[0]}")
        print(f"DEBUG {self.sw_name} | elected = {self.elected_attr}")
        print(f"DEBUG {self.sw_name} | promised = {self.promised_attr}")
        print()
        cpu_header = CPU_header(ingress_port = elected[3])
        packet[IP].remove_payload()
        packet[IP].proto = CPU_HEADER_PROTO

        # Update packets payload info
        data = "destination=" + dst
        data = data + " | distance=" + str(elected[1] + 1)
        data = data + " | seq_no=" + str(elected[2])
        pad = Padding()
        pad.load = data
        packet = packet / cpu_header / pad
        iface = self.topo.get_interfaces(self.sw_name)[0]
        sendp(packet, iface=iface, verbose=False)

    #Returns an elected or promised attribute that corresponds to a given Destination
    #dst : string -> node's name
    #type : string -> "elected" or "promised"
    def search_stored_attr(self, dst, type:str):
        if not(type == "elected" or type == "promised"):
            raise AssertionError('Type must be elected or promised')

        if type == "elected":
            for host in self.elected_attr:
                if dst == host:
                    return self.elected_attr[dst]
        elif type == "promised":
            for host in self.promised_attr:
                if dst == host:
                    return self.promised_attr[dst]
        return None

    #This function will update or add a new attribute in the elected or promised attributes
    # attr : list[] -> list with [distance, seq_no, port]
    #type : string -> "elected" or "promised"
    def save_attribute(self, dst, attr, type:str):
        if not len(attr) == 3:
            raise AssertionError('attr must have length 3: [distance, seq_no, port]')
        if not(type == "elected" or type == "promised"):
            raise AssertionError('Type must be elected or promised')

        if type == "elected":
            self.elected_attr[dst] = attr
            return
        elif type == "promised":
            self.promised_attr[dst] = attr
            return

    def delete_promised(self, dst):
        attr = [float('inf'), self.elected_attr[dst][1]+1, 0]
        self.promised_attr[dst] = attr
        return

    # returns True if first is better than second
    # type : string -> says which type of metric it is (distance, congestion ...)
    def compare_metric(self, first, second, type):
        if type == "distance" or type == "delay":
            return first < second

        elif type == "capacity" or type == "bandwidth":
            return first > second

        raise AssertionError('This metric type is unknwon')

    # This function will save the attribute in the elected_attr dict
    # and modify the ipv4_lpm table
    def elect_attribute(self,dst, attr):
        neighbor = self.topo.port_to_node(self.sw_name, attr[2])
        dst_mac = self.topo.node_to_node_mac(self.sw_name, neighbor)
        self.save_attribute(dst, attr, "elected")
        success = self.controller.table_modify_match("ipv4_lpm", "ipv4_forward",
                                [dst], [dst_mac, str(attr[2])])
        #print("DEBUG: {} | Adding new ipv4 rule for dst= {} and port={} ".format(self.sw_name,dst,ingress_port))
        self.delete_promised(dst)
        return success


    #This function will decide if the new attribute is to be elected, promised or discarded
    # Returns True if the attribute is elected
    def make_decision(self, sw, packetIn_params):
        dst_addr = packetIn_params[0]
        distance = packetIn_params[1]
        seq_no = packetIn_params[2]
        ingress_port = packetIn_params[3]
        attr = [distance, seq_no, ingress_port]

        elected = self.search_stored_attr(dst_addr, "elected")
        promised = self.search_stored_attr(dst_addr, "promised")

        # New computation when ingress_port is the cpu port
        if ingress_port == self.cpu_port:
            self.save_attribute(dst_addr, attr, "elected")
            promised = [float('inf'), self.elected_attr[dst_addr][1]+1, 0]
            self.save_attribute(dst_addr, promised, "promised")
            print(f"DEBUG: {self.sw_name} | Starting a new computation for destination {dst_addr}")
            return packetIn_params

        #destination unknown
        elif elected is None:
            neighbor = self.topo.port_to_node(self.sw_name, ingress_port)
            dst_mac = self.topo.node_to_node_mac(self.sw_name, neighbor)
            self.save_attribute(dst_addr, attr, "elected")
            self.controller.table_add("ipv4_lpm", "ipv4_forward",
                                    [dst_addr], [dst_mac, str(ingress_port)])
            distance_pro = float('inf')
            attr_pro = (distance_pro, seq_no+1, 0)
            # add an infinite promised for the new destination
            self.save_attribute(dst_addr, attr_pro, "promised")
            print (f"DEBUG: {self.sw_name} | Elected attribute for a new destination")
            return packetIn_params

        # same next hop as the elected
        elif ingress_port == elected[2]:
            if seq_no > promised[1]:
                self.save_attribute(dst_addr, attr, "elected")
                self.delete_promised(dst_addr)
                print(f"DEBUG: {self.sw_name} | Same attribute as the elected, more recent than promised")
                return packetIn_params
            elif seq_no == promised[1]:
                if self.compare_metric(distance, promised[0], "distance"):
                    self.save_attribute(dst_addr, attr, "elected")
                    self.delete_promised(dst_addr)
                    print(f"DEBUG: {self.sw_name} | Same attribute as the elected, same computation as promised")
                    return packetIn_params
                else:
                    self.elect_attribute(dst_addr, promised)
                    print(f"DEBUG: {self.sw_name} | elected got worse, promised elected")
                    promised.insert(0,dst_addr)
                    return promised

        # same next hop as the promised
        elif ingress_port == promised[2]:
            if self.compare_metric(distance, elected[0], "distance"):
                self.elect_attribute(dst_addr, attr)
                print(f"DEBUG: {self.sw_name} | promised got better, is now the elected")
                return packetIn_params
            else:
                self.save_attribute(dst_addr, attr, "promised")
                print(f"DEBUG: {self.sw_name} | promised got updated")
                return None

        # Different next hop
        else:
            if seq_no > promised[1]:
                if self.compare_metric(distance, elected[0], "distance"):
                    self.elect_attribute(dst_addr, attr)
                    print(f"DEBUG: {self.sw_name} | new attribute elected more recent than promised")
                    return packetIn_params
                else:
                    self.save_attribute(dst_addr, attr, "promised")
                    print(f"DEBUG: {self.sw_name} | new promised")
                    return None
            elif seq_no == promised[1]:
                if self.compare_metric(distance, elected[0], "distance"):
                    self.elect_attribute(dst_addr, attr)
                    self.delete_promised(dst_addr)
                    print(f"DEBUG: {self.sw_name} | new attribute elected with same seq_no as promised")
                    return packetIn_params
                elif distance < promised[0]:
                    self.save_attribute(dst_addr, attr, "promised")
                    print(f"DEBUG: {self.sw_name} | promised changed with a better attribute from the same computation")
                    return None
        #otherwise discard
        print(f"DEBUG: {self.sw_name} | This probe will be discarded")
        return None

if __name__ == "__main__":
    import sys
    sw_name = sys.argv[1]
    controller = Controller(sw_name).run()
