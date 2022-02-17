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
            {hdr.ipv4.protocol, meta.destination},
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
        clone3(CloneType.I2E, 100, meta);
    }

    action get_registers_info() {
        // Read elected distance
        elected_distance.read(meta.E_distance, meta.register_index);
        // Read elected sequence number
        elected_seq_num.read(meta.E_seq_no, meta.register_index);
        //Read elected next hop
        elected_NH.read(meta.E_NH, meta.register_index);

        //Read promised distance
        promised_distance.read(meta.P_distance, meta.register_index);
        //Read promised sequence number
        promised_seq_num.read(meta.P_seq_no, meta.register_index);
        //Read promised next hop
        promised_NH.read(meta.P_NH, meta.register_index);
    }

    action elect_attribute() {
        elected_distance.write(meta.register_index, hdr.probe.distance);
        elected_seq_num.write(meta.register_index, hdr.probe.seq_no);
        elected_NH.write(meta.register_index, standard_metadata.ingress_port);

        // No promised yet so distance is infinite
        promised_distance.write(meta.register_index, (bit<16>) 9999);
        promised_seq_num.write(meta.register_index, hdr.probe.seq_no + 1);
        promised_NH.write(meta.register_index, (bit<9>) 0);

        // update metadata
        meta.E_distance = hdr.probe.distance;
        meta.E_seq_no = hdr.probe.seq_no;
        meta.E_NH = standard_metadata.ingress_port;

        // Update probe's distance to broadcast it
        hdr.probe.distance = meta.E_distance + 1;
    }

    action elect_promise() {
        elected_distance.write(meta.register_index, meta.P_distance);
        elected_seq_num.write(meta.register_index, meta.P_seq_no);
        elected_NH.write(meta.register_index, meta.P_NH);

        // Update probe to broadcast it
        hdr.probe.distance = meta.P_distance + 1;
        hdr.probe.seq_no = meta.P_seq_no;

        // No promised yet so distance is infinite
        promised_distance.write(meta.register_index, (bit<16>) 9999);
        promised_seq_num.write(meta.register_index, meta.P_seq_no + 1);
        promised_NH.write(meta.register_index, (bit<9>) 0);

        // update metadata
        meta.E_distance = meta.P_distance;
        meta.E_seq_no = meta.P_seq_no;
        meta.E_NH = meta.P_NH;
    }

    action change_promise() {
        promised_distance.write(meta.register_index, hdr.probe.distance);
        promised_seq_num.write(meta.register_index, hdr.probe.seq_no);
        promised_NH.write(meta.register_index, standard_metadata.ingress_port);
    }

    table check_destination_known {
        key = {
            hdr.probe.destination: lpm;
        }
        actions = {
            get_registers_info;
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

                    switch (check_destination_known.apply().action_run){
                        // Destination unknown
                        elect_attribute: {
                            meta.new_destination = true;
                            update_table();
                        }

                        // Go through the 3 cases
                        get_registers_info: {

                            // Starting a new computation
                            if (hdr.probe.distance == 0){
                                elect_attribute();
                                broadcast_elected_attr.apply();
                            }

                            // Same Next Hop as the elected
                            if (standard_metadata.ingress_port == meta.E_NH){
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
            if (meta.new_destination == true){
                hdr.cpu.new_destination = 1;
            }
            else{
                hdr.cpu.new_destination = 0;
            }
            hdr.ipv4.protocol = CPU_HEADER_PROTO;
            truncate((bit<32>) 40); // ether+ipv4+cpu header
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
