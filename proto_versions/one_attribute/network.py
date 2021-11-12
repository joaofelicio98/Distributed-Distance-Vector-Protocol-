from p4utils.mininetlib.network_API import NetworkAPI

net = NetworkAPI()

# Network general options
net.setLogLevel('info')
net.setCompiler(p4rt=True)
net.execScript('python controllerv2.py s1 &', reboot=True)
net.execScript('python controllerv2.py s2 &', reboot=True)
net.execScript('python controllerv2.py s3 &', reboot=True)

# Network definition
net.addP4RuntimeSwitch('s1')
net.addP4RuntimeSwitch('s2')
net.addP4RuntimeSwitch('s3')
net.setP4SourceAll('./p4src/main.p4')
net.addHost('h1')
net.addHost('h2')
net.addHost('h3')
net.addLink('s1', 'h1', port1=1)
net.addLink('s2', 'h2', port1=1)
net.addLink('s3', 'h3', port1=1)
net.addLink('s1', 's2', port1=2, port2=2)
net.addLink('s1', 's3', port1=3, port2=2)
net.addLink('s2', 's3', port1=3, port2=3)

# Assignment strategy
net.mixed()


# Nodes general options
net.enableCpuPortAll()
net.enablePcapDumpAll()
net.enableLogAll()
net.enableCli()
net.startNetwork()
