from time import sleep
from scapy.all import *

from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI

CPU_HEADER_PROTO = 253
MY_HEADER_PROTO = 254
topo = load_topo('topology.json')
controllers = {} # {sw_name: seq_no}

def start_computation(dst_addr, sw_name, seq_no, port): #sendProbe()
    print ("DEBUG: Starting a new computation for subnet ", dst_addr)

    iface = topo.get_ctl_cpu_intf(sw_name)

    data = "destination=" + str(dst_addr)
    data = data + " | distance=0 | seq_no=" + str(seq_no)
    pad = Padding()
    pad.load = data

    packet = Ether(src=get_if_hwaddr(str(topo.get_cpu_port_intf(sw_name))), dst='ff:ff:ff:ff:ff:ff')
    packet = packet / IP(proto=MY_HEADER_PROTO) / pad
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
                    host = topo.get_hosts_connected_to(sw)[0]
                    subnet = topo.subnet(host,sw)
                    start_computation(subnet, sw, controllers[sw], topo.get_cpu_port_index(sw))
                    controllers[sw] = controllers[sw] + 1

            elif c in controllers:
                host = topo.get_hosts_connected_to(c)[0]
                subnet = topo.subnet(host,c)
                print("Subnet: ",subnet)
                start_computation(subnet, c, controllers[c], topo.get_cpu_port_index(c))

            elif c == 'lol':
                print(topo.get_interfaces_to_node('s1'))
            else:
                raise AssertionError('This command does not exist')



    except KeyboardInterrupt:
        print()
        print("Ending probes delivery.")

if __name__ == "__main__":
    main()
