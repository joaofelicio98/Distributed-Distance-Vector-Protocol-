from p4utils.mininetlib.network_API import NetworkAPI

net = NetworkAPI()

net.setLogLevel("info")
net.setCompiler(p4rt=True)
net.disableArpTables()

net.execScript("python controller.py s1 &", reboot=True)
net.addP4RuntimeSwitch("s1")
net.addHost("h1")
net.execScript("python controller.py s2 &", reboot=True)
net.addP4RuntimeSwitch("s2")
net.addHost("h2")
net.execScript("python controller.py s3 &", reboot=True)
net.addP4RuntimeSwitch("s3")
net.addHost("h3")
net.execScript("python controller.py s4 &", reboot=True)
net.addP4RuntimeSwitch("s4")
net.addHost("h4")
net.execScript("python controller.py s5 &", reboot=True)
net.addP4RuntimeSwitch("s5")
net.addHost("h5")
net.execScript("python controller.py s6 &", reboot=True)
net.addP4RuntimeSwitch("s6")
net.addHost("h6")
net.execScript("python controller.py s7 &", reboot=True)
net.addP4RuntimeSwitch("s7")
net.addHost("h7")
net.execScript("python controller.py s8 &", reboot=True)
net.addP4RuntimeSwitch("s8")
net.addHost("h8")
net.execScript("python controller.py s9 &", reboot=True)
net.addP4RuntimeSwitch("s9")
net.addHost("h9")
net.execScript("python controller.py s10 &", reboot=True)
net.addP4RuntimeSwitch("s10")
net.addHost("h10")
net.execScript("python controller.py s11 &", reboot=True)
net.addP4RuntimeSwitch("s11")
net.addHost("h11")
net.setP4SourceAll("./p4src/main.p4")

net.addLink("s1", "h1")
net.addLink("s2", "h2")
net.addLink("s3", "h3")
net.addLink("s4", "h4")
net.addLink("s5", "h5")
net.addLink("s6", "h6")
net.addLink("s7", "h7")
net.addLink("s8", "h8")
net.addLink("s9", "h9")
net.addLink("s10", "h10")
net.addLink("s11", "h11")

net.addLink("s1", "s2")
net.setDelay("s1", "s2", 41)
net.setBw("s1", "s2", 0.001)
net.addLink("s1", "s3")
net.setDelay("s1", "s3", 43)
net.setBw("s1", "s3", 0.001)
net.addLink("s2", "s11")
net.setDelay("s2", "s11", 44)
net.setBw("s2", "s11", 0.001)
net.addLink("s3", "s10")
net.setDelay("s3", "s10", 38)
net.setBw("s3", "s10", 0.001)
net.addLink("s4", "s5")
net.setDelay("s4", "s5", 33)
net.setBw("s4", "s5", 0.001)
net.addLink("s4", "s7")
net.setDelay("s4", "s7", 60)
net.setBw("s4", "s7", 0.001)
net.addLink("s5", "s6")
net.setDelay("s5", "s6", 63)
net.setBw("s5", "s6", 0.001)
net.addLink("s5", "s7")
net.setDelay("s5", "s7", 65)
net.setBw("s5", "s7", 0.001)
net.addLink("s6", "s9")
net.setDelay("s6", "s9", 53)
net.setBw("s6", "s9", 0.001)
net.addLink("s7", "s8")
net.setDelay("s7", "s8", 37)
net.setBw("s7", "s8", 0.001)
net.addLink("s8", "s9")
net.setDelay("s8", "s9", 34)
net.setBw("s8", "s9", 0.001)
net.addLink("s8", "s11")
net.setDelay("s8", "s11", 45)
net.setBw("s8", "s11", 0.001)
net.addLink("s9", "s10")
net.setDelay("s9", "s10", 46)
net.setBw("s9", "s10", 0.001)
net.addLink("s10", "s11")
net.setDelay("s10", "s11", 75)
net.setBw("s10", "s11", 0.001)
# Assignment strategy
net.mixed()
# Nodes general options
net.enableCpuPortAll()
net.enablePcapDumpAll()
net.enableLogAll()
net.enableCli()
net.startNetwork()
