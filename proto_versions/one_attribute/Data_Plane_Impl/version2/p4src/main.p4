/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>
#include "include/headers.p4"
#include "include/parsers.p4"

#define REGISTER_SIZE 1024


/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {

    register<bit<16>>(REGISTER_SIZE) elected_distance;
    register<bit<32>>(REGISTER_SIZE) elected_seq_num;
    register<bit<9>>(REGISTER_SIZE) elected_NH;

    register<bit<16>>(REGISTER_SIZE) promised_distance;
    register<bit<32>>(REGISTER_SIZE) promised_seq_num;
    register<bit<9>>(REGISTER_SIZE) promised_NH;

    action drop() {
        mark_to_drop(standard_metadata);
    }

    action get_registers_index() {
        // Compute register index
        hash(meta.register_index,
            HashAlgorithm.crc32,
            (bit<32>)0,
            {hdr.ipv4.protocol, hdr.probe.destination},
            (bit<32>)1024);
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

    // Action called to modify the ipv4_lpm table
    action update_table() {
        meta.destination = hdr.probe.destination;
        clone3(CloneType.I2E, 100, meta);
    }

    action get_info(bit<9> next_hop, bit<14> distance, bit<32> seq_no) {

    }

    action elect_attribute(bit<9> cpu_port) {
        hdr.cpu.setValid();
        hdr.cpu.destination = hdr.probe.destination;
        hdr.cpu.next_hop = standard_metadata.ingress_port;
        hdr.cpu.new_destination = 1;
        hdr.cpu.distance = hdr.probe.distance;
        hdr.cpu.seq_no = hdr.probe.seq_no;
        hdr.probe.setInvalid();
        hdr.ipv4.protocol = CPU_HEADER_PROTO;

        standard_metadata.egress_spec = port;
    }

    table check_destination {
        key = {
            hdr.probe.destination: lpm;
        }
        actions = {
            get_info;
            elect_attribute;
        }
        size = 1024;
        default_action = elect_attribute;
    }

    action set_mcast_grp(bit<16> mcast_id) {
        standard_metadata.mcast_grp = mcast_id;
    }

    table broadcast_elected_attr {
        key = {
            meta.E_NH: exact;
        }
        actions = {
            set_mcast_grp;
            drop;
        }
        size = 1024;
        default_action = drop;
    }

    apply {

        if (hdr.ipv4.isValid()){
            if (hdr.ipv4.protocol != PROBE_PROTO){
                ipv4_lpm.apply();
            }
            @atomic{
                if(hdr.ipv4.protocol == PROBE_PROTO && hdr.probe.isValid()){
                    get_registers_index();
                    meta.new_destination = false;

                    switch (check_destination_known.apply().action_run){
                        // Destination unknown
                        elect_attribute: {
                    //if (!check_destination_known.apply().hit){
                            meta.new_destination = true;
                            update_table();
                            broadcast_elected_attr.apply();
                        }

                        // Go through the 3 cases
                        get_registers_info: {
                    //else {

                            // Starting a new computation
                            if (hdr.probe.distance == 0){
                                elect_attribute();
                                broadcast_elected_attr.apply();
                            }

                            // Same Next Hop as the elected
                            else if (standard_metadata.ingress_port == meta.E_NH){
                                if (hdr.probe.seq_no > meta.P_seq_no){
                                    elect_attribute();
                                    broadcast_elected_attr.apply();
                                }
                                else if (hdr.probe.seq_no == meta.P_seq_no){
                                    if (hdr.probe.distance <= meta.P_distance){
                                        elect_attribute();
                                        broadcast_elected_attr.apply();
                                    }
                                    else{
                                        elect_promise();
                                        broadcast_elected_attr.apply();
                                    }
                                }
                            }

                            // Same Next Hop as the promised
                            else if(standard_metadata.ingress_port == meta.P_NH){
                                if (hdr.probe.distance < meta.E_distance) {
                                    elect_attribute();
                                    meta.test = (bit<8>) 1;
                                    update_table();
                                    broadcast_elected_attr.apply();
                                }
                                else {
                                    change_promise();
                                }
                            }

                            // Different Next Hop
                            else {
                                if (hdr.probe.seq_no > meta.P_seq_no) {
                                    if (hdr.probe.distance < meta.E_distance){
                                        elect_attribute();
                                        meta.test = (bit<8>) 2;
                                        update_table();
                                        broadcast_elected_attr.apply();
                                    }
                                    else{
                                        change_promise();
                                    }
                                }
                                else if (hdr.probe.seq_no == meta.P_seq_no) {
                                    if (hdr.probe.distance < meta.E_distance) {
                                        elect_attribute();
                                        meta.test = (bit<8>) 3;
                                        update_table();
                                        broadcast_elected_attr.apply();
                                    }
                                    else if (hdr.probe.distance < meta.P_distance){
                                        change_promise();
                                    }
                                }
                            }
                        }
                    }
                }
            }
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

        // If ingress clone
        if(standard_metadata.instance_type == 1){
            hdr.probe.setInvalid();
            hdr.cpu.setValid();
            hdr.cpu.destination = meta.destination;
            hdr.cpu.next_hop = (bit<16>) meta.E_NH;
            hdr.cpu.test = meta.test;
            if (meta.new_destination == true){
                hdr.cpu.new_destination = (bit<8>) 1;
            }
            else{
                hdr.cpu.new_destination = (bit<8>) 0;
            }
            hdr.ipv4.protocol = CPU_HEADER_PROTO;
            truncate((bit<32>) 45); // ether+ipv4+cpu header
        }
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
