#!/usr/bin/env python2
import argparse
import grpc
import os
import sys
import ctypes
from time import sleep
from scapy.all import *
import threading

from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI

CPU_HEADER_PROTO = 253
TOLERANCE = 2

class CPU_header(Packet):
    name = 'CPU'
    fields_desc = [IPField('dst_addr','127.0.0.1'), BitField('distance',0,16),
                   BitField('seq_no',0,32), BitField('ingress_port', 0, 16)]

class ControllerThread(Thread):

    def __init__(self, sw_name, lock):
        threading.Thread.__init__(self)
        self.topo = load_topo('topology.json')
        self.sw_name = sw_name
        self.lock = lock
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
        self.elected_attr = []
        #stored promised attributes -> {destination:  [distance,seq_no,port]}
        self.promised_attr = []
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
        self.add_clone_session()
        self.send_first_computation()
        #create a new thread to start a new computation in x by x seconds
        thread = threading.Thread(target=self.send_new_computation, args=())
        thread.daemon = True
        thread.start()


    def add_boadcast_groups(self):
        interfaces_to_port = self.topo.get_node_intfs(fields=['port'])[self.sw_name].copy()
        # Filter lo and cpu port
        interfaces_to_port.pop('lo', None)
        interfaces_to_port.pop(self.topo.get_cpu_port_intf(self.sw_name), None)

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

    def add_CPU_rules(self):
        self.controller.table_add("cpu_table", "send_to_cpu", [str(CPU_HEADER_PROTO)])

    def add_clone_session(self):
        if self.cpu_port:
            self.controller.cs_create(100, [self.cpu_port])

    def start_computation(self, dst, seq_no, port, new):
        print ("DEBUG: Starting a new computation for destination ", dst)

        dstAddr = self.topo.get_host_ip(dst)

        #save attribute on dictionary elected_attr
        attr = [0, seq_no, port]
        self.save_attribute(dstAddr, attr, "elected", new)

        cpu_header = CPU_header(dst_addr = dstAddr, distance = 0,
                                seq_no = seq_no, ingress_port = port)

        bind_layers(IP, CPU_header, proto = CPU_HEADER_PROTO)

        cpu_port_intf = str(self.topo.get_cpu_port_intf(self.sw_name).replace("eth0", "eth1"))

        packet = Ether(src=get_if_hwaddr(cpu_port_intf), dst='ff:ff:ff:ff:ff:ff')
        packet = packet /IP(src=dstAddr, proto=CPU_HEADER_PROTO)/cpu_header
        packet.show2()

        iface = self.topo.get_cpu_port_intf(self.sw_name)

        sendp(packet, iface=iface, verbose=False)

    def send_first_computation(self):
        with self.lock:

            hosts = self.topo.get_hosts_connected_to(self.sw_name)

            for host in hosts:
                port = self.topo.node_to_node_port_num(self.sw_name, host)
                self.start_computation(host, 1, port, True)

    def send_new_computation(self):
        while True:
            sleep(1000) #wait 1 minutes
            with self.lock:
                #print ("DEBUG: Acquired lock in send_new_computation")

                nodes = self.topo.get_nodes(fields=['isHost'])
                for node in list(nodes):
                    if not nodes[node]:
                        del nodes[node]

                for host in list(nodes):
                    list = self.search_stored_attr(host, "elected")
                    seq_no = list[1] + 1
                    port = list[2]
                    self.start_computation(host, seq_no, port, False)

    # Main loop of the thread
    def run(self):
        try:
            sleep(0.2)
            while True:
                cpu_port_intf = str(self.topo.get_cpu_port_intf(self.sw_name).replace("eth0", "eth1"))
                print("DEBUG: sniffing at port: {}".format(cpu_port_intf))
                sniff(iface=cpu_port_intf, prn=self.recv_msg_cpu)
        finally:
            print("Ending controller {}".format(self.sw_name))

#TODO nao esta a receber os pacotes
    def recv_msg_cpu(self, pkt):
        print('DEBUG: recebeu novo pacote!')
        with self.lock:
            packet = IP(raw(pkt))
            if packet.protocol == CPU_HEADER_PROTO:
                print("DEBUG: Received a new attribute!")
                cpu_header = CPU_header(bytes(packet.load))
                if (self.make_decision([(cpu_header.dst_addr, cpu_header.distance,
                                    cpu_header.seq_no, cpu_header.ingress_port)])):
                    self.announce_attribute(pkt)

    def announce_attribute(self, packet):
        print("DEBUG: announcing an elected attribute")
        iface = self.topo.get_cpu_port_intf(self.sw_name)
        sendp(packet, iface=iface, verbose=False)

    #Get the name of the neighbor attached to the given port
    def port_to_neighbor_name(port):
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
            for attr in self.elected_attr:
                if dst in attr:
                    return attr[dst]
        elif type == "promised":
            for attr in self.promised_attr:
                if dst in attr:
                    return attr[dst]
        return None

    #This function will update or add a new attribute in the elected or promised attributes
    # attr : list[] -> list with [distance, seq_no, port]
    #type : string -> "elected" or "promised"
    #new : boolean -> True if it is a new destination to add, False if it is to update
    def save_attribute(self, dst, attr, type:str, new:bool):
        if not len(attr) == 3:
            raise AssertionError('attr must have length 3: [distance, seq_no, port]')
        if not(type == "elected" or type == "promised"):
            raise AssertionError('Type must be elected or promised')
        #if not(type(new) == bool):
        #    raise AssertionError("Parameter new must be type boolean")

        if new:
            if type == "elected":
                self.elected_attr.append({dst:attr})
                return
            elif type == "promised":
                self.promised_attr.append({dst:attr})
                return
        else:
            if type == "elected":
                for i in range(len(self.elected_attr)):
                    if dst in self.elected_attr[i]:
                        self.elected_attr[i][dst] = attr
                        return
            elif type == "promised":
                for i in range(len(self.promised_attr)):
                    if dst in self.promised_attr[i]:
                        self.promised_attr[i][dst] = attr
                        return

    def delete_promised(dst):
        for i in range(len(self.promised_attr)):
            if dst in self.promised_attr[i]:
                del self.promised_attr[i]
                return

    #This function will decide if the new attribute is to elected, promised or discarded
    # Returns True if the attribute is elected
    def make_decision(p4info_helper, topo_utils, sw, packetIn_params):
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
            self.save_attribute(dst_addr, attr, "elected", True)
            self.controller.table_add("ipv4_lpm", "ipv4_forward",
                                    [dst_addr], [dst_mac, ingress_port])
            print ("DEBUG: Elected attribute for a new destination")
            return True

        # Packet received is from an older computation -> discard
        elif elected[1] > seq_no:
            print ("DEBUG: Older sequence number -> discard")
            return False

        # Better metric and >= sequence number -> always elect
        elif compare_metric(distance, elected[0], "distance") and seq_no >= elected[1]:
            save_attribute(dst_addr, attr, "elected", False)
            # Different next hop -> change forwarding table
            if ingress_port != elected[2]:
                neighbor = self.port_to_neighbor_name(ingress_port)
                dst_mac = self.topo.node_to_node_mac(self.sw_name, neighbor)
                self.controller.table_modify_match("ipv4_lpm", "ipv4_forward",
                                        [dst_addr], [dst_mac, ingress_port])
            if promised is not None:
                if seq_no >= promised[1]:
                    self.delete_promised(dst_addr)
            print ("DEBUG: Elected new attribute with better metric and >= seq_no")
            return True

        # If sequence number is much more recent should always elect
        elif seq_no - elected[1] > TOLERANCE:
            self.save_attribute(dst_addr, attr, "elected", False)
            if ingress_port != elected[2]:
                neighbor = self.port_to_neighbor_name(ingress_port)
                dst_mac = self.topo.node_to_node_mac(self.sw_name, neighbor)
                self.controller.table_modify_match("ipv4_lpm", "ipv4_forward",
                                        [dst_addr], [dst_mac, ingress_port])
            if promised is not None:
                self.delete_promised(dst_addr)
            print ("DEBUG: Elected new attribute with much more recent seq_no")
            return True

        # Same next hop as the elected
        elif ingress_port == elected[2]:
            # Sequence number more recent than the elected or equal
            # Worse metric -> there was a change in the topology
            if self.compare_metric(elected[0], distance, "distance"):
                if promised is not None:
                    # Compare with promised first
                    if self.compare_metric(distance, promised[0], "distance"):
                        self.save_attribute(dst_addr, attr, "elected", False)
                        print ("DEBUG: elected attribute with worse metric, same next hop")
                        return True
                    # elect promised
                    else:
                        self.save_attribute(dst_addr, promised, "elected", False)
                        neighbor = self.port_to_neighbor_name(ingress_port)
                        dst_mac = self.topo.node_to_node_mac(self.sw_name, neighbor)
                        self.controller.table_modify_match("ipv4_lpm", "ipv4_forward",
                                                [dst_addr], [dst_mac, promised[2]])
                        self.delete_promised(dst_addr)
                        print ("DEBUG Elected promised attribute")
                        return True
                else:
                    self.save_attribute(dst_addr, attr, "elected", False)
                    print ("DEBUG: Attribute with worse metric, same next hop, no promised")
                    return True
            # Same attribute as the elected only with a more recent sequence number
            else:
                self.save_attribute(dst_addr, attr, "elected", False)
                print ("DEBUG: Same attribute, more recent seq_no")
                if promised is not None:
                    if seq_no >= promised[1]:
                        self.delete_promised(dst_addr)
                        print ("DEBUG: Also deleted promised")
                return True

        # Different next hop
        # The condition with better metric is already checked so only <= metric
        # is missing at this point : action -> save in promised_attr or do nothing
        else:
            # Different next hop than promised
            if promised is not None:
                if seq_no > promised[1]:
                    self.save_attribute(dst_addr, attr, "promised", False)
                    print ("DEBUG: Changed promised, better seq_no")
                elif ingress_port != promised[2]:
                    if self.compare_metric(distance, promised[0], "distance"):
                        self.save_attribute(dst_addr, attr, "promised", False)
                        print ("DEBUG: Changed promised, better metric")
            else:
                self.save_attribute(dst_addr, attr, "promised", True)
                print ("DEBUG: New promised added, there was no promised for this destination")
            return False


    #returns the ID of the respective thread
    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                ctypes.py_object(SystemExit))

        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

#TODO: This class will temporarilly read all match-action tables from every controller
class Debugger:

    def __init__(self, controllers):
        self.controllers = controllers

    def run_loop(self):
        try:
            while True:
                continue
        except KeyboardInterrupt:
            print (" Shutting down.")
            for c in controllers:
                c.raise_exception()

if __name__ == "__main__":
    #testing
    #import sys
    #sw_name = sys.argv[1]
    #controller = ControllerThread(sw_name).run()

    topo = load_topo('topology.json')

    nodes = topo.get_nodes(fields=['isSwitch'])
    for node in list(nodes):
        if node == 'sw-cpu' or not nodes[node]:
            del nodes[node]


    # creating a controller per P4switch
    controllers = []
    for sw in list(nodes):
        # creating a lock
        lock = threading.Lock()
        controller = ControllerThread(sw, lock)
        controller.start()
        controllers.append(controller)

    # debugger for reading all tables
    debugger = Debugger(controllers).run_loop()
