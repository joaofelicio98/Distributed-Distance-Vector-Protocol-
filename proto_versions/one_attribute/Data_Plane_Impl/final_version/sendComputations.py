from time import sleep
from scapy.all import *

from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI

CPU_HEADER_PROTO = 253
MY_HEADER_PROTO = 254
topo = load_topo('topology.json')
controllers = {} # {sw_name: seq_no}

class Probe_header(Packet):
    name = 'Probe'
    fields_desc = [IPField('destination', '127.0.0.1'),
                    BitField('distance',0,16), BitField('seq_no',0,32)]

def get_if(sw):
    hosts = topo.get_hosts_connected_to(sw)
    interfaces = topo.get_node_intfs(fields=['port'])[sw].copy()
    iface = ""
    for intf, port in interfaces.items():
        if hosts[0] in intf:
            iface = intf
            break
    print(f"INTFFFFF:  {iface}")

    return iface

def start_computation(dst_addr, sw_name, seq_no): #sendProbe()
    print ("DEBUG: Starting a new computation for subnet ", dst_addr)

    #iface = get_if(sw_name)
    iface = topo.get_ctl_cpu_intf(sw_name)
    print(f"DEBUG:  destination = {dst_addr} | seq_no = {seq_no}")

    probe_header = Probe_header(destination = dst_addr, distance = 0, seq_no = seq_no)
    packet = Ether(src=get_if_hwaddr(str(iface)), dst='ff:ff:ff:ff:ff:ff')
    packet = packet / IP(proto=MY_HEADER_PROTO) / probe_header
    packet.show2()

    print("DEBUG: sending to interface: {}".format(iface))
    sendp(packet, iface=iface, verbose=False)


def main():
    try:
        dict = topo.get_p4rtswitches(fields=['isSwitch'])

        for sw_name, value in dict.items():
            if value:
                controllers[sw_name] = 1

        print("DEBUG: Controllers: ",controllers)
        print()

        while True:
            for sw_name, value in controllers.items():
                print("Press {} to send a new probe for {} subnet".format(sw_name,sw_name))
            print("Or press x to send a new probe for every subnet")
            c = input("Press your command...")

            if c == 'x':
                for sw in controllers:
                    """
                    host = topo.get_hosts_connected_to(sw)[0]
                    subnet = topo.subnet(host,sw)
                    start_computation(subnet, sw, controllers[sw])
                    controllers[sw] = controllers[sw] + 1
                    """
                    host = topo.get_hosts_connected_to(sw)[0]
                    #dst_ip = topo.node_to_node_interface_ip(host,sw)
                    dst_ip = topo.get_host_ip(host)
                    start_computation(dst_ip, sw, controllers[sw])
                    controllers[sw] = controllers[sw] + 1
                    #sleep(0.7)

            elif c in controllers:
                """
                host = topo.get_hosts_connected_to(c)[0]
                subnet = topo.subnet(host,c)
                print("Subnet: ",subnet)
                start_computation(subnet, c, controllers[c])
                """
                host = topo.get_hosts_connected_to(c)[0]
                #dst_ip = topo.node_to_node_interface_ip(host,sw)
                dst_ip = topo.get_host_ip(host)
                start_computation(dst_ip, c, controllers[c])
                controllers[c] = controllers[c] + 1
            else:
                print("Invalid command")



    except KeyboardInterrupt:
        print()
        print("Ending probes delivery.")

if __name__ == "__main__":
    main()
