import json
import random

name = ""
nodes = []
links = []
index = 0
with open("GtsCe.json","r") as f:

    for line in f:
        stripped = line.strip()
        if "Network " in stripped and "NetworkDate" not in stripped:
            name = stripped.removeprefix("Network ").replace('"', '')
        elif "id " in stripped and "_id" not in stripped:
            nodes.append(int(stripped.removeprefix("id "))+1)
        elif "source" in stripped:
            links.append([int(stripped.removeprefix("source "))])
        elif "target" in stripped:
            links[index].append(int(stripped.removeprefix("target ")))
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

    f.write('\n')
    for node in nodes:
        f.write(f'net.addLink("s{node}", "h{node}")\n')

    f.write('\n')
    for link in links:
        f.write(f'net.addLink("s{link[0]}", "s{link[1]}")\n')
        delay = random.randint(25,75)
        f.write(f'net.setDelay("s{link[0]}", "s{link[1]}", {delay})\n')
        f.write(f'net.setBw("s{link[0]}", "s{link[1]}", 0.001)\n')
