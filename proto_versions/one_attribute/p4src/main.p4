/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>
#include "include/headers.p4"
#include "include/parsers.p4"


/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
    action drop() {
        mark_to_drop(standard_metadata);
    }


    action ipv4_forward(macAddr_t dstAddr, egressSpec_t port) {
        standard_metadata.egress_spec = port;
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dstAddr;
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }

    table ipv4_lpm {
        key = {
            hdr.ipv4.dstAddr: lpm;
        }
        actions = {
            ipv4_forward;
            //send;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = drop;
    }

    action send_to_cpu(egressSpec_t cpu_port) {
        hdr.ipv4.protocol = CPU_HEADER_PROTO;
        hdr.cpu.setValid();
        hdr.cpu.ingress_port = (bit<16>)standard_metadata.ingress_port;
        standard_metadata.egress_spec = cpu_port;
    }

//for now it will always send to the CPU, it may do other actions
//in the dataplane when I transfer some logic down here
    table cpu_table {
        key = {
            hdr.ipv4.protocol: exact;
        }
        actions = {
            send_to_cpu;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = drop;
    }

    action set_mcast_grp(bit<16> mcast_id) {
        standard_metadata.mcast_grp = mcast_id;
    }

    table broadcast_elected_attr {
        key = {
            meta.ingress_port: exact;
        }
        actions = {
            set_mcast_grp;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = drop;
    }

    apply {

        if (hdr.cpu.isValid()) {
            meta.ingress_port = (bit<9>)hdr.cpu.ingress_port;
            hdr.cpu.setInvalid();
            hdr.ipv4.protocol = MY_HEADER_PROTO;
            broadcast_elected_attr.apply();
        }

        else if (hdr.ipv4.protocol == MY_HEADER_PROTO) {
            cpu_table.apply();
        }
        else if (hdr.ipv4.isValid()) {
            ipv4_lpm.apply();
        }
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply {
     }
}


/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;
