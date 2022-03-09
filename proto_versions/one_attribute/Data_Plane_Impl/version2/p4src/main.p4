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

    register<bit<16>>(REGISTER_SIZE) elected_distance_1;
    register<bit<16>>(REGISTER_SIZE) elected_distance_2;
    register<bit<32>>(REGISTER_SIZE) elected_seq_no_1;
    register<bit<32>>(REGISTER_SIZE) elected_seq_no_2;

    register<bit<16>>(REGISTER_SIZE) promised_distance_1;
    register<bit<16>>(REGISTER_SIZE) promised_distance_2;
    register<bit<32>>(REGISTER_SIZE) promised_seq_no_1;
    register<bit<32>>(REGISTER_SIZE) promised_seq_no_2;
    register<bit<9>>(REGISTER_SIZE) promised_NH_1;
    register<bit<9>>(REGISTER_SIZE) promised_NH_2;

    counter(1024, CounterType.packets) packet_counter;


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

    action send_to_cpu(bit<9> cpu_port) {
        standard_metadata.egress_spec = cpu_port;

        hdr.probe.setInvalid();
        hdr.cpu.setValid();
        hdr.cpu.destination = meta.destination;
        hdr.cpu.next_hop = (bit<15>) meta.E_NH;
        if (meta.is_new == true){
            hdr.cpu.is_new = (bit<1>) 1;
        }
        else{
            hdr.cpu.is_new = (bit<1>) 0;
        }
        hdr.cpu.info = meta.register_index;
        hdr.cpu.test = meta.test;
        hdr.ipv4.protocol = CPU_HEADER_PROTO;
    }

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

    // Action called to modify the ipv4_lpm table
    action update_table() {
        clone3(CloneType.I2E, 100, meta);
    }

    action elect_attribute_2() {
        elected_distance_2.write(meta.register_index, hdr.probe.distance);
        elected_seq_no_2.write(meta.register_index, hdr.probe.seq_no);
        promised_distance_2.write(meta.register_index, 9999);
        promised_seq_no_2.write(meta.register_index, hdr.probe.seq_no + 1);
        promised_NH_2.write(meta.register_index, 0);

        meta.E_distance = hdr.probe.distance;
        meta.E_seq_no = hdr.probe.seq_no;
        meta.E_NH = standard_metadata.ingress_port;

        //hdr.probe.distance = hdr.probe.distance + 1;
    }

    action elect_attribute_1() {
        elected_distance_1.write(meta.register_index, hdr.probe.distance);
        elected_seq_no_1.write(meta.register_index, hdr.probe.seq_no);
        promised_distance_1.write(meta.register_index, 9999);
        promised_seq_no_1.write(meta.register_index, hdr.probe.seq_no + 1);
        promised_NH_1.write(meta.register_index, 0);

        meta.E_distance = hdr.probe.distance;
        meta.E_seq_no = hdr.probe.seq_no;
        meta.E_NH = standard_metadata.ingress_port;

        //hdr.probe.distance = hdr.probe.distance + 1;
    }

    action elect_promise_2() {

        elected_distance_2.write(meta.register_index, meta.P_distance);
        elected_seq_no_2.write(meta.register_index, meta.P_seq_no);
        promised_distance_2.write(meta.register_index, 9999);
        promised_seq_no_2.write(meta.register_index, meta.P_seq_no + 1);
        promised_NH_2.write(meta.register_index, 0);

        meta.E_seq_no = meta.P_seq_no;
        meta.E_distance = meta.P_distance;
        meta.E_NH = meta.P_NH;
    }

    action elect_promise_1() {
        elected_distance_1.write(meta.register_index, meta.P_distance);
        elected_seq_no_1.write(meta.register_index, meta.P_seq_no);
        promised_distance_1.write(meta.register_index, 9999);
        promised_seq_no_1.write(meta.register_index, meta.P_seq_no + 1);
        promised_NH_1.write(meta.register_index, 0);

        meta.E_seq_no = meta.P_seq_no;
        meta.E_distance = meta.P_distance;
        meta.E_NH = meta.P_NH;
    }

    action change_promise_2() {
        elected_distance_2.write(meta.register_index, meta.E_distance);
        elected_seq_no_2.write(meta.register_index, meta.E_seq_no);
        promised_distance_2.write(meta.register_index, hdr.probe.distance);
        promised_seq_no_2.write(meta.register_index, hdr.probe.seq_no);
        promised_NH_2.write(meta.register_index, standard_metadata.ingress_port);
    }

    action change_promise_1() {
        elected_distance_1.write(meta.register_index, meta.E_distance);
        elected_seq_no_1.write(meta.register_index, meta.E_seq_no);
        promised_distance_1.write(meta.register_index, hdr.probe.distance);
        promised_seq_no_1.write(meta.register_index, hdr.probe.seq_no);
        promised_NH_1.write(meta.register_index, standard_metadata.ingress_port);
    }

    action get_info(bit<9> next_hop, bit<32> p_counter) {
        meta.destination = hdr.probe.destination;
        meta.packet_counter = p_counter;
        meta.E_NH = next_hop;
    }

    action read_registers_1() {
        elected_distance_1.read(meta.E_distance, meta.register_index);
        elected_seq_no_1.read(meta.E_seq_no, meta.register_index);

        promised_distance_1.read(meta.P_distance, meta.register_index);
        promised_seq_no_1.read(meta.P_seq_no, meta.register_index);
        promised_NH_1.read(meta.P_NH, meta.register_index);
    }

    action read_registers_2() {
        elected_distance_2.read(meta.E_distance, meta.register_index);
        elected_seq_no_2.read(meta.E_seq_no, meta.register_index);

        promised_distance_2.read(meta.P_distance, meta.register_index);
        promised_seq_no_2.read(meta.P_seq_no, meta.register_index);
        promised_NH_2.read(meta.P_NH, meta.register_index);
    }

    action elect_new_destination() {
        elected_distance_1.write(meta.register_index, hdr.probe.distance);
        elected_seq_no_1.write(meta.register_index, hdr.probe.seq_no);

        promised_distance_1.write(meta.register_index, 9999);
        promised_seq_no_1.write(meta.register_index, hdr.probe.seq_no + 1);
        promised_NH_1.write(meta.register_index, 0);

        meta.destination = hdr.probe.destination;
        meta.E_distance = hdr.probe.distance;
        meta.E_seq_no = hdr.probe.seq_no;
        meta.E_NH = standard_metadata.ingress_port;

        //hdr.probe.distance = hdr.probe.distance + 1;
        meta.is_new = true;
    }

    table check_destination_known {
        key = {
            hdr.probe.destination: lpm;
        }
        actions = {
            get_info;
            elect_new_destination;
        }
        size = 1024;
        default_action = elect_new_destination;
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

        @atomic{
            if (hdr.ipv4.isValid() && hdr.ipv4.ttl > 0){
                // Data packets
                if (hdr.ipv4.protocol != PROBE_PROTO && hdr.ipv4.protocol != CPU_HEADER_PROTO){
                    ipv4_lpm.apply();
                }
                // Packets sent by the cpu to broadcast
                else if (hdr.ipv4.protocol == CPU_HEADER_PROTO && hdr.cpu.isValid()) {
                    get_registers_index();

                    hdr.cpu.setInvalid();
                    hdr.probe.setValid();

                    if(hdr.cpu.info % 2 == 0){
                        read_registers_1();
                    }else{
                        read_registers_2();
                    }

                    hdr.probe.destination = hdr.cpu.destination;
                    hdr.probe.distance = meta.E_distance + 1;
                    hdr.probe.seq_no = meta.E_seq_no;
                    hdr.ipv4.protocol = PROBE_PROTO;

                    broadcast_elected_attr.apply();
                }
                // Probe received from a broadcast
                else if(hdr.ipv4.protocol == PROBE_PROTO && hdr.probe.isValid()){
                    get_registers_index();
                    meta.is_new = false;

                    switch (check_destination_known.apply().action_run){
                        // Destination unknown
                        elect_new_destination: {
                            meta.test = (bit<8>) 1;
                            //update_table();
                            //broadcast_elected_attr.apply();
                            cpu_table.apply();
                        }

                        // Go through the 3 cases
                        get_info: {

                            if(meta.packet_counter % 2 == 0){
                                read_registers_1();
                            }else{
                                read_registers_2();
                            }

                            // Starting a new computation
                            if (hdr.probe.distance == 0){
                                if(meta.packet_counter % 2 == 0) {
                                    elect_attribute_2();
                                }else{
                                    elect_attribute_1();
                                }
                                if (hdr.probe.seq_no == 1){
                                    update_table(); // For the controller to get the counter index
                                    //cpu_table.apply();
                                }
                                packet_counter.count(meta.register_index);
                                broadcast_elected_attr.apply();
                            }

                            // Same Next Hop as the elected
                            else if (standard_metadata.ingress_port == meta.E_NH){
                                if (hdr.probe.seq_no > meta.P_seq_no){
                                    if(meta.packet_counter % 2 == 0) {
                                        elect_attribute_2();
                                    }else{
                                        elect_attribute_1();
                                    }
                                    packet_counter.count(meta.register_index);
                                    broadcast_elected_attr.apply();
                                }
                                else if (hdr.probe.seq_no == meta.P_seq_no){
                                    if (hdr.probe.distance <= meta.P_distance){
                                        if(meta.packet_counter % 2 == 0) {
                                            elect_attribute_2();
                                        }else{
                                            elect_attribute_1();
                                        }
                                        packet_counter.count(meta.register_index);
                                        broadcast_elected_attr.apply();
                                    }
                                    else{
                                        if(meta.packet_counter % 2 == 0) {
                                            elect_promise_2();
                                        }else{
                                            elect_promise_1();
                                        }
                                        packet_counter.count(meta.register_index);
                                        meta.test = (bit<8>) 3;
                                        //update_table();
                                        //broadcast_elected_attr.apply();
                                        cpu_table.apply();
                                    }
                                }
                            }

                            // Same Next Hop as the promised
                            else if(standard_metadata.ingress_port == meta.P_NH){
                                if (hdr.probe.distance < meta.E_distance) {
                                    if(meta.packet_counter % 2 == 0) {
                                        elect_attribute_2();
                                    }else{
                                        elect_attribute_1();
                                    }
                                    packet_counter.count(meta.register_index);
                                    meta.test = (bit<8>) 4;
                                    //update_table();
                                    //broadcast_elected_attr.apply();
                                    cpu_table.apply();
                                }
                                else {
                                    if(meta.packet_counter % 2 == 0) {
                                        change_promise_2();
                                    }else{
                                        change_promise_1();
                                    }
                                    packet_counter.count(meta.register_index);
                                }
                            }

                            // Different Next Hop
                            else {
                                if (hdr.probe.seq_no > meta.P_seq_no) {
                                    if (hdr.probe.distance < meta.E_distance){
                                        if(meta.packet_counter % 2 == 0) {
                                            elect_attribute_2();
                                        }else{
                                            elect_attribute_1();
                                        }
                                        packet_counter.count(meta.register_index);
                                        meta.test = (bit<8>) 5;
                                        //update_table();
                                        //broadcast_elected_attr.apply();
                                        cpu_table.apply();
                                    }
                                    else{
                                        if(meta.packet_counter % 2 == 0) {
                                            change_promise_2();
                                        }else{
                                            change_promise_1();
                                        }
                                        packet_counter.count(meta.register_index);
                                    }
                                }
                                else if (hdr.probe.seq_no == meta.P_seq_no) {
                                    if (hdr.probe.distance < meta.E_distance) {
                                        if(meta.packet_counter % 2 == 0) {
                                            elect_attribute_2();
                                        }else{
                                            elect_attribute_1();
                                        }
                                        packet_counter.count(meta.register_index);
                                        meta.test = (bit<8>) 6;
                                        //update_table();
                                        //broadcast_elected_attr.apply();
                                        cpu_table.apply();
                                    }
                                    else if (hdr.probe.distance < meta.P_distance){
                                        if(meta.packet_counter % 2 == 0) {
                                            change_promise_2();
                                        }else{
                                            change_promise_1();
                                        }
                                        packet_counter.count(meta.register_index);
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
            hdr.cpu.next_hop = (bit<15>) meta.E_NH;
            hdr.cpu.info = meta.register_index;
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
