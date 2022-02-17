from scapy.all import *

CPU_HEADER_PROTO = 253

class CPU_header(Packet):
    name = 'CPU'
    fields_desc = [BitField('ingress_port', 0, 16)]

def decodeNum(encoded_number):
    return int(encoded_number.hex(), 16)

def bitwidthToBytes(bitwidth):
    return int(math.ceil(bitwidth / 8.0))

def encodeNum(number, bitwidth):
    byte_len = bitwidthToBytes(bitwidth)
    num_str = '%x' % number
    if number >= 2 ** bitwidth:
        raise Exception("Number, %d, does not fit in %d bits" % (number, bitwidth))
    return bytes.fromhex('0' * (byte_len * 2 - len(num_str)) + num_str)

def main():

    dstAddr = "10.0.0.1"
    seq_no = 2
    port = 4

    cpu_header = CPU_header(ingress_port = port)

    bind_layers(IP, CPU_header, proto = CPU_HEADER_PROTO)

    data = "destination=" + str(dstAddr)
    data = data + " | distance=0 | seq_no=" + str(seq_no)
    data = data + " | port=" + str(port)

    packet = Ether(dst='ff:ff:ff:ff:ff:ff')
    packet = packet / IP(src=dstAddr, proto=CPU_HEADER_PROTO) / cpu_header / data
    packet.show2()

    #data = str(packet[Raw].load)
    #distance = data.rsplit(" | ")[1].rsplit("=")[1]
    #print(distance)
    #seq_no = data.rsplit(" | ")[2].rsplit("=")[1]
    #print(seq_no)
    #port = data.rsplit(" | ")[3].rsplit("=")[1]
    #print(port)

    packet[Raw].load = "destination=23.14.43.4 | distance=23 | seq_no=5 | port=690"
    packet.show2()
    print()
    #cpu_header = CPU_header(bytes(packet.load))
    #print(cpu_header.ingress_port)
    print(packet[CPU_header].ingress_port)
    print()
    print(packet.load)
    #packet = Ether(raw(packet))
    #cpu_header = CPU_header(bytes(packet.load))
    #print("port: ",packet[CPU_header].ingress_port)
    #print(packet[Raw])

if __name__ == "__main__":
    main()
