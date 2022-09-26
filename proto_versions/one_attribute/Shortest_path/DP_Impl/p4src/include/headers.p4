const bit<16> TYPE_IPV4 = 0x800;
const bit<16> TYPE_ARP = 0x806;
const bit<8> TCP_PROTOCOL = 6;
const bit<8> UDP_PROTOCOL = 17;
const bit<8> PROBE_PROTO = 254;
const bit<8> CPU_HEADER_PROTO = 253;

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

header arp_t {          //TODO fazer tabelas para tratar dos pacotes ARP
    bit<16> hwType16;
    bit<16> protoType;
    bit<8> hwAddrLen;
    bit<8> protoAddrLen;
    bit<16> opcode;
    bit<48> hwSrcAddr;
    bit<32> protoSrcAddr;
    bit<48> hwDstAddr;
    bit<32> protoDstAddr;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

// Header used to clone packets to the cpu
header cpu_t {
    ip4Addr_t destination;
    //bit<16>   distance;
    bit<32>   seq_no;
    bit<9>    port;
    bit<1>    is_new;
    bit<6>    flag;
}

header probe_t {
    ip4Addr_t destination;
    bit<16>   distance;
    bit<32>   seq_no;
}

header tcp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<32> seqNo;
    bit<32> ackNo;
    bit<4> dataOffset;
    bit<3> res;
    bit<3> ecn;
    bit<6> ctrl;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgentPtr;
}

header udp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<16> length;
    bit<16> checksum;
}


struct metadata {
    bit<32>     register_index;
    bool        is_new;
    ip4Addr_t   destination;

    bit<16>     E_distance;
    bit<32>     E_seq_no;
    bit<9>      E_NH;

    bit<6>      flag;
}

struct headers {
    ethernet_t   ethernet;
    arp_t        arp;
    ipv4_t       ipv4;
    cpu_t        cpu;
    probe_t      probe;
    tcp_t        tcp;
    udp_t        udp;
}
