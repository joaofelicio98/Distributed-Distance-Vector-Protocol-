import sys
from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_p4runtime_API import SimpleSwitchP4RuntimeAPI
from p4utils.utils.thrift_API import ThriftAPI

class Library():

    def __init__(self, sw_name):
        self.topo = load_topo('topology.json')
        self.sw_name = sw_name
        self.cpu_port = self.topo.get_cpu_port_index(self.sw_name)
        device_id = self.topo.get_p4switch_id(sw_name)
        grpc_port = self.topo.get_grpc_port(sw_name)
        sw_data = self.topo.get_p4rtswitches()[sw_name]
        self.controller = SimpleSwitchP4RuntimeAPI(device_id, grpc_port,
                                                   p4rt_path=sw_data['p4rt_path'],
                                                   json_path=sw_data['json_path'])
        thrift_port = self.topo.get_thrift_port(self.sw_name)
        self.controller_thrift = ThriftAPI(thrift_port)

    def run(self):
        while True:
            print("Press REGISTER <name> to read the values of a register")
            print()
            print("Press your command...")
            c = sys.stdin.readline()

            if c.rsplit(" ")[0] == "REGISTER":
                name = c.rsplit(" ")[1]
                self.read_register(name)

    def read_register(self, name):
        result = self.controller_thrift.register_read(name, None, True)
        print(result)

if __name__ == "__main__":
    import sys
    sw_name = sys.argv[1]
    lib = Library(sw_name).run()
