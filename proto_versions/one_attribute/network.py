from p4utils.mininetlib.network_API import NetworkAPI

net = NetworkAPI()

# Network general options
net.setLogLevel('info')
net.setCompiler(p4rt=True)
#net.execScript('python controller2.py s1 &', reboot=True)
#net.execScript('python controller2.py s2 &', reboot=True)
#net.execScript('python controller2.py s3 &', reboot=True)
#net.execScript('python controller2.py s4 &', reboot=True)

# Network definition
net.addP4RuntimeSwitch('s1')
net.addP4RuntimeSwitch('s2')
net.addP4RuntimeSwitch('s3')
net.addP4RuntimeSwitch('s4')
net.setP4SourceAll('./p4src/main.p4')
net.addHost('h1')
net.addHost('h2')
net.addHost('h3')
net.addHost('h4')
net.addLink('s1', 'h1', port1=1)
net.addLink('s2', 'h2', port1=1)
net.addLink('s3', 'h3', port1=1)
net.addLink('s4', 'h4', port1=1)
net.addLink('s1', 's2', port1=2, port2=2)
net.addLink('s1', 's3', port1=3, port2=2)
net.addLink('s1', 's4', port1=4, port2=2)
net.addLink('s2', 's4', port1=3, port2=3)
net.addLink('s3', 's4', port1=3, port2=4)

# Assignment strategy
net.mixed()
#net.setIntfIp('h1','s1','10.0.1.10/24')
#net.setIntfIp('h2','s2','10.0.2.20/24')
#net.setIntfIp('h3','s3','10.0.3.30/24')
#net.setIntfIp('h4','s4','10.0.4.40/24')



# Nodes general options
net.enableCpuPortAll()
net.enablePcapDumpAll()
net.enableLogAll()
net.enableCli()
net.startNetwork()
