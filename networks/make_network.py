import json
import random

name = ""
nodes = []
links = []
index = 0
min_delay=108
max_delay=132
with open("IRISNetworks","r") as f:

    for line in f:
        stripped = line.strip()
        if "Network " in stripped and "NetworkDate" not in stripped:
            name = stripped.replace("Network ","").replace('"', '').replace(" ","")
        elif "id " in stripped and "_id" not in stripped and "e" not in stripped:
            nodes.append(int(stripped.replace("id ",""))+1)
        elif "source" in stripped:
            links.append([int(stripped.replace("source ",""))+1])
        elif "target" in stripped:
            links[index].append(int(stripped.replace("target ",""))+1)
            index+=1

with open(f"{name}.py","w") as f:
    f.write('from p4utils.mininetlib.network_API import NetworkAPI\n')
    f.write('\n')
    f.write('net = NetworkAPI()\n')
    f.write('\n')
    f.write('net.setLogLevel("info")\n')
    f.write('net.setCompiler(p4rt=True)\n')
    f.write('net.disableArpTables()\n')
    f.write('\n')

    for node in nodes:
        f.write(f'net.execScript("python controller.py s{node} &", reboot=True)\n')
        f.write(f'net.addP4RuntimeSwitch("s{node}")\n')
        f.write(f'net.addHost("h{node}")\n')
    f.write('net.setP4SourceAll("./p4src/main.p4")\n')

    f.write('\n')
    for node in nodes:
        f.write(f'net.addLink("s{node}", "h{node}")\n')

    f.write('\n')
    for link in links:
        f.write(f'net.addLink("s{link[0]}", "s{link[1]}")\n')
        delay = random.randint(min_delay,max_delay)
        f.write(f'net.setDelay("s{link[0]}", "s{link[1]}", {delay})\n')
        f.write(f'net.setBw("s{link[0]}", "s{link[1]}", 1)\n')

    f.write('# Assignment strategy\n')
    f.write('net.mixed()\n')
    f.write('# Nodes general options\n')
    f.write('net.enableCpuPortAll()\n')
    f.write('#net.enablePcapDumpAll()\n')
    f.write('#net.enableLogAll()\n')
    f.write('net.enableCli()\n')
    f.write('net.startNetwork()\n')
