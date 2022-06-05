import sys

if len(sys.argv) != 2:
    raise  AssertionError("Must specify the name of the networks's script")

network_script = f"{sys.argv[1]}.py"
delays = {}
bws = {}

with open(network_script, 'r') as f:
    for line in f:
        if  "net.setDelay" in line:
            node1 = line.rsplit(",")[0][-3:].replace("'","")
            node2 = line.rsplit(",")[1][-3:].replace("'","")
            delay = line.rsplit(",")[2].replace(")","")
            delays[f"{node1}-{node2}"] = delay[:-1]
        elif "net.setBw" in line:
            node1 = line.rsplit(",")[0][-3:].replace("'","")
            node2 = line.rsplit(",")[1][-3:].replace("'","")
            bw = line.rsplit(",")[2].replace(")","")[:-1]
            bws[f"{node1}-{node2}"] = bw

with open('links_data.txt', 'w') as file:
    for link,delay in delays.items():
         file.write(f"{link} > delay={delay}\n")
    for link,bw in bws.items():
        file.write(f"{link} > bandwidth={bw}\n")
