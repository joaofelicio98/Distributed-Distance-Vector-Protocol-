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
            node_name = self.port_to_neighbor_name(ingress_port)
            if node_name in self.topo.get_hosts():
                intf_to_pop.append(intf)
        for intf in intf_to_pop:
            interfaces_to_port.pop(intf, None)

        for ingress_port in interfaces_to_port.values():
            port_list = list(interfaces_to_port.values())
            del(port_list[port_list.index(ingress_port)])

            # Add multicast group and ports
            for port in port_list:
                intf_name = self.sw_name + '-eth' + str(port)
                node = self.topo.interface_to_node(self.sw_name, intf_name)
                if self.topo.isHost(node):
                    del(port_list[port_list.index(port)])

            self.controller.mc_mgrp_create(ingress_port, port_list)

            # Fill broadcast table
            #print ("DEBUG: creating mcastgrp: {} for ports: {}".format(ingress_port, port_list))
            self.controller.table_add("broadcast_elected_attr", "set_mcast_grp", [str(ingress_port)], [str(ingress_port)])

        self.controller.mc_mgrp_create(100, list(interfaces_to_port.values()))
        self.controller.table_add("broadcast_elected_attr", "set_mcast_grp", [str(100)], [str(100)])

    #IPv4 rules for every host connected to the switch
    def add_initial_ipv4_rules(self):
        neighbors = self.topo.get_neighbors(self.sw_name)

        for node in neighbors:
            if self.topo.isHost(node):
                dst_ip = self.topo.node_to_node_interface_ip(node, self.sw_name)
                dst_ip = dst_ip.rsplit('/')[0]
                dst_mac = self.topo.node_to_node_mac(node, self.sw_name)
                port = self.topo.node_to_node_port_num(self.sw_name, node)
                self.controller.table_add("ipv4_lpm", "ipv4_forward", [dst_ip], [dst_mac, str(port)])
                #self.elected_attr[dst_ip] = [0, 1, port]
                #self.promised_attr[dst_ip] = [float('inf'), 2, 0]

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
                print("DEBUG: {} | sniffing at port: {}".format(self.sw_name, cpu_port_intf))
                sniff(iface=cpu_port_intf, prn=self.recv_msg_cpu)
        except KeyboardInterrupt:
            print("Ending controller {}".format(self.sw_name))
            self.reset()

    def recv_msg_cpu(self, pkt):
        #print('DEBUG: {} | Received a new packet!'.format(self.sw_name))
        #print(pkt[IP].proto)
        if pkt[IP].proto == CPU_HEADER_PROTO:
            print("DEBUG: {} | Received a new attribute!".format(self.sw_name))
            #print()
            #pkt.show2()
            #print()
            pkt = Ether(raw(pkt))
            cpu_header = CPU_header(bytes(pkt.load))
            port = cpu_header.ingress_port
            #port = pkt[CPU_header].ingress_port
            data = str(pkt[Raw].load)
            dst = data.rsplit(" | ")[0].rsplit("=")[1]
            distance = int(data.rsplit(" | ")[1].rsplit("=")[1])
            seq_no = int(data.rsplit(" | ")[2].rsplit("=")[1][:-1])
            print("DEBUG: {} | destination = {} | distance = {}| seq_no = {} | port = {}".format(self.sw_name,dst,distance,seq_no,port))
            #print("DEBUG: {} | distance = {}".format(self.sw_name,distance))
            #print("DEBUG: {} | seq_no = {}".format(self.sw_name,seq_no))
            #print("DEBUG: {} | port = {}".format(self.sw_name,port))
            params = [dst, distance, seq_no, port]
            if self.make_decision(self.sw_name, params):
                self.announce_attribute(pkt, params)

#TODO: Se for port=0 mandar para todos os outros  switches vizinhos
    def announce_attribute(self, packet, params):
        print("DEBUG: {} | announcing an elected attribute for subnet {}".format(self.sw_name, params[0]))
        #print("DEBUG: {} | distance = {}".format(self.sw_name, params[1]))
        #print("DEBUG: {} | sequence number = {}".format(self.sw_name, params[2]))
        #print("DEBUG: {} | port = {}".format(self.sw_name, params[3]))

        #packet.show2()
        cpu_header = CPU_header(ingress_port = params[3])
        packet[IP].remove_payload()

        # Update packets payload info
        data = "destination=" + params[0]
        data = data + " | distance=" + str(params[1] + 1)
        data = data + " | seq_no=" + str(params[2])

        packet = packet / cpu_header / data
        packet.show2()
        iface = self.topo.get_cpu_port_intf(self.sw_name)
        sendp(packet, iface=iface, verbose=False)

#TODO: iface before assignment
    #Get the name of the neighbor attached to the given port
    def port_to_neighbor_name(self, port):
        interfaces_to_port = self.topo.get_node_intfs(fields=['port'])[self.sw_name].copy()
        for intf in interfaces_to_port:
            if interfaces_to_port[intf] == port:
                iface = intf
        neighbor = self.topo.interface_to_node(self.sw_name, iface)
        return neighbor

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
    def elect_attribute(self, ingress_port, dst, attr):
        neighbor = self.port_to_neighbor_name(ingress_port)
        dst_mac = self.topo.node_to_node_mac(self.sw_name, neighbor)
        self.save_attribute(dst, attr, "elected")
        success = self.controller.table_modify_match("ipv4_lpm", "ipv4_forward",
                                [dst], [dst_mac, str(ingress_port)])
        #print("DEBUG: {} | Adding new ipv4 rule for dst= {} and port={} ".format(self.sw_name,dst,ingress_port))
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

        #destination unknown
        if elected is None:
            neighbor = self.port_to_neighbor_name(ingress_port)
            dst_mac = self.topo.node_to_node_mac(self.sw_name, neighbor)
            self.save_attribute(dst_addr, attr, "elected")
            self.controller.table_add("ipv4_lpm", "ipv4_forward",
                                    [dst_addr], [dst_mac, str(ingress_port)])
            distance_pro = float('inf')
            attr_pro = (distance_pro, seq_no+1, 0)
            # add an infinite promised for the new destination
            self.save_attribute(dst_addr, attr_pro, "promised")
            print ("DEBUG: {} | Elected attribute for a new destination".format(self.sw_name))
            print()
            #print("DEBUG: {} | Adding new ipv4 rule for dst= {} and port={} ".format(self.sw_name,dst_addr,ingress_port))
            return True

        # same next hop as the elected
        elif ingress_port == elected[2]:

            if seq_no > promised[1]:
                self.save_attribute(dst_addr, attr, "elected")
                self.delete_promised(dst_addr)
                print("DEBUG: {} | Same attribute as the elected, more recent than promised".format(self.sw_name))
                print()
                return True

            elif seq_no == promised[1]:

                if self.compare_metric(distance, promised[0], "distance"):
                    self.save_attribute(dst_addr, attr, "elected")
                    self.delete_promised(dst_addr)
                    print("DEBUG: {} | Same attribute as the elected, same computation as promised".format(self.sw_name))
                    print()
                    return True

                else:
                    self.elect_attribute(ingress_port, dst_addr, promised)
                    self.delete_promised(dst_addr)
                    print("DEBUG: {} | elected got worse, promised elected".format(self.sw_name))
                    print()
                    return True

        # same next hop as the promised
        elif ingress_port == promised[2]:

            if self.compare_metric(distance, elected[0], "distance"):
                self.elect_attribute(ingress_port, dst_addr, attr)
                self.delete_promised(dst_addr)
                print("DEBUG: {} | promised got better, is now the elected".format(self.sw_name))
                print()
                return True

            else:
                self.save_attribute(dst_addr, attr, "promised")
                print("DEBUG: {} | promised got updated".format(self.sw_name))
                print()
                return

        # Different next hop
        else:

            if seq_no > promised[1]:

                if self.compare_metric(distance, elected[0], "distance"):
                    self.elect_attribute(ingress_port, dst_addr, attr)
                    self.delete_promised(dst_addr)
                    print("DEBUG: {} | new attribute elected more recent than promised".format(self.sw_name))
                    print()
                    return True

                else:
                    self.save_attribute(dst_addr, attr, "promised")
                    print("DEBUG: {} | new promised".format(self.sw_name))
                    print()
                    return

            elif seq_no == promised[1]:

                if self.compare_metric(distance, elected[0], "distance"):
                    self.elect_attribute(ingress_port, dst_addr, attr)
                    self.delete_promised(dst_addr)
                    print("DEBUG: {} | new attribute elected with same seq_no as promised".format(self.sw_name))
                    print()
                    return True

                elif distance < promised[0]:
                    self.save_attribute(dst_addr, attr, "promised")
                    print("DEBUG: {} | promised changed with a better attribute from the same computation".format(self.sw_name))
                    print()
                    return
        #otherwise discard
        print("DEBUG: {} | This probe will be discarded".format(self.sw_name))
        print()
        return

if __name__ == "__main__":
    import sys
    sw_name = sys.argv[1]
    controller = Controller(sw_name).run()