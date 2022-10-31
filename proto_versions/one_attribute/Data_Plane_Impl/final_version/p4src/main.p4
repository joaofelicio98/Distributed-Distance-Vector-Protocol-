/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>
#include "include/headers.p4"
#include "include/parsers.p4"

#define REGISTER_SIZE 4096 


/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {

    register<bit<16>>(REGISTER_SIZE) elected_distance;
    register<bit<32>>(REGISTER_SIZE) elected_seq_num;
    register<bit<8>>(REGISTER_SIZE) elected_NH;

    register<bit<16>>(REGISTER_SIZE) promised_distance;
    register<bit<32>>(REGISTER_SIZE) promised_seq_num;
    register<bit<8>>(REGISTER_SIZE) promised_NH;

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
        size = 2048;
        default_action = drop;
    }

    // This action is used to send elected attributes to the controller
    action update_table() {
        meta.destination = hdr.probe.destination;
        clone3(CloneType.I2E, 100, meta);
    }

    // Get all info about the elected and promised attributes for the given destination
    action get_info() {
        // Read elected distance
        elected_distance.read(meta.E_distance, meta.register_index);
        //Read elected next hop
        elected_NH.read(meta.E_NH, meta.register_index);

        //Read promised distance
        promised_distance.read(meta.P_distance, meta.register_index);
        //Read promised sequence number
        promised_seq_num.read(meta.P_seq_no, meta.register_index);
        //Read promised next hop
        promised_NH.read(meta.P_NH, meta.register_index);
    }

    // Elect the received attribute
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

        // No promised yet so distance is infinite
        promised_distance.write(meta.register_index, (bit<16>) 9999);
        promised_seq_num.write(meta.register_index, meta.P_seq_no + 1);
        promised_NH.write(meta.register_index, (bit<9>) 0);

        // update metadata
        meta.E_distance = meta.P_distance;
        meta.E_seq_no = meta.P_seq_no;
        meta.E_NH = meta.P_NH;

        // Update probe's distance to broadcast it
        hdr.probe.distance = meta.E_distance + 1;
    }

    action change_promise() {
        promised_distance.write(meta.register_index, hdr.probe.distance);
        promised_seq_num.write(meta.register_index, hdr.probe.seq_no);
        promised_NH.write(meta.register_index, standard_metadata.ingress_port);
    }

    action set_mcast_grp(bit<16> mcast_id) {
        standard_metadata.mcast_grp = mcast_id;
    }

    table broadcast_elected_attr {
        key = {
            meta.E_NH : exact;
        }
        actions = {
            set_mcast_grp;
            drop;
        }
        size = 2048;
        default_action = drop;
    }

    apply {

        if (hdr.ipv4.isValid()){
            // Data packets
            if (hdr.ipv4.protocol != PROBE_PROTO){
                ipv4_lpm.apply();
            }
            else if(hdr.ipv4.protocol == PROBE_PROTO && hdr.probe.isValid()){
                get_registers_index();
                meta.destination = hdr.probe.destination;
                meta.is_new = false;
                // Read elected sequence number
                elected_seq_num.read(meta.E_seq_no, meta.register_index);

                // If True means that there is no information on the registers yet
                if(meta.E_seq_no == 0){
                    // Starting a new computation
                    if (hdr.probe.distance == 0){
                        elect_attribute();
                        meta.flag = 20;
                        update_table();
                        broadcast_elected_attr.apply();
                    }else{
                        // Destination unknown
                        meta.is_new = true;
                        elect_attribute();
                        update_table();
                        broadcast_elected_attr.apply();
                    }
                }

                // Go through the 3 cases
                else{
                    get_info();

                    // Check for link failure cases
                    if (hdr.probe.seq_no - meta.E_seq_no > 2){
                        elect_attribute();
                        meta.flag = 10;
			            update_table();
                        broadcast_elected_attr.apply();
                    }

                    // Starting a new computation
                    else if (hdr.probe.distance == 0){
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
                            meta.flag = 1;
                            update_table();
                            broadcast_elected_attr.apply();
                        }
                        else {
                            change_promise();
                        }
                    }

                    // Different Next Hop
                    else {
			if (hdr.probe.seq_no == meta.E_seq_no) {
			    if (hdr.probe.distance < meta.E_distance){
				elect_attribute();
				meta.flag = 4;
				update_table();
				broadcast_elected_attr.apply();
			    }
			}
                        else if (hdr.probe.seq_no > meta.P_seq_no) {
                            if (hdr.probe.distance < meta.E_distance){
                                elect_attribute();
                                meta.flag = 2;
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
                                meta.flag = 3;
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
            hdr.cpu.seq_no = meta.E_seq_no;
            hdr.cpu.next_hop = meta.E_NH;
            hdr.cpu.flag = meta.flag;
            if (meta.is_new == true){
                hdr.cpu.is_new = 1;
            }
            else{
                hdr.cpu.is_new = 0;
            }
            hdr.ipv4.protocol = CPU_HEADER_PROTO;
            truncate((bit<32>) 44); // ether+ipv4+cpu_header
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
