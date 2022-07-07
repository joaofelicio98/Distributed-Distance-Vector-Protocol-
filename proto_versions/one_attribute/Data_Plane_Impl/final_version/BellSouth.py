from p4utils.mininetlib.network_API import NetworkAPI

net = NetworkAPI()

net.setLogLevel("info")
net.setCompiler(p4rt=True)
net.disableArpTables()

#net.execScript("python controller.py s1 &", reboot=True)
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
net.execScript("python controller.py s12 &", reboot=True)
net.addP4RuntimeSwitch("s12")
net.addHost("h12")
net.execScript("python controller.py s13 &", reboot=True)
net.addP4RuntimeSwitch("s13")
net.addHost("h13")
net.execScript("python controller.py s14 &", reboot=True)
net.addP4RuntimeSwitch("s14")
net.addHost("h14")
net.execScript("python controller.py s15 &", reboot=True)
net.addP4RuntimeSwitch("s15")
net.addHost("h15")
net.execScript("python controller.py s16 &", reboot=True)
net.addP4RuntimeSwitch("s16")
net.addHost("h16")
net.execScript("python controller.py s17 &", reboot=True)
net.addP4RuntimeSwitch("s17")
net.addHost("h17")
net.execScript("python controller.py s18 &", reboot=True)
net.addP4RuntimeSwitch("s18")
net.addHost("h18")
net.execScript("python controller.py s19 &", reboot=True)
net.addP4RuntimeSwitch("s19")
net.addHost("h19")
net.execScript("python controller.py s20 &", reboot=True)
net.addP4RuntimeSwitch("s20")
net.addHost("h20")
net.execScript("python controller.py s21 &", reboot=True)
net.addP4RuntimeSwitch("s21")
net.addHost("h21")
net.execScript("python controller.py s22 &", reboot=True)
net.addP4RuntimeSwitch("s22")
net.addHost("h22")
net.execScript("python controller.py s23 &", reboot=True)
net.addP4RuntimeSwitch("s23")
net.addHost("h23")
net.execScript("python controller.py s24 &", reboot=True)
net.addP4RuntimeSwitch("s24")
net.addHost("h24")
net.execScript("python controller.py s25 &", reboot=True)
net.addP4RuntimeSwitch("s25")
net.addHost("h25")
net.execScript("python controller.py s26 &", reboot=True)
net.addP4RuntimeSwitch("s26")
net.addHost("h26")
net.execScript("python controller.py s27 &", reboot=True)
net.addP4RuntimeSwitch("s27")
net.addHost("h27")
net.execScript("python controller.py s28 &", reboot=True)
net.addP4RuntimeSwitch("s28")
net.addHost("h28")
net.execScript("python controller.py s29 &", reboot=True)
net.addP4RuntimeSwitch("s29")
net.addHost("h29")
net.execScript("python controller.py s30 &", reboot=True)
net.addP4RuntimeSwitch("s30")
net.addHost("h30")
net.execScript("python controller.py s31 &", reboot=True)
net.addP4RuntimeSwitch("s31")
net.addHost("h31")
net.execScript("python controller.py s32 &", reboot=True)
net.addP4RuntimeSwitch("s32")
net.addHost("h32")
net.execScript("python controller.py s33 &", reboot=True)
net.addP4RuntimeSwitch("s33")
net.addHost("h33")
net.execScript("python controller.py s34 &", reboot=True)
net.addP4RuntimeSwitch("s34")
net.addHost("h34")
net.execScript("python controller.py s35 &", reboot=True)
net.addP4RuntimeSwitch("s35")
net.addHost("h35")
net.execScript("python controller.py s36 &", reboot=True)
net.addP4RuntimeSwitch("s36")
net.addHost("h36")
net.execScript("python controller.py s37 &", reboot=True)
net.addP4RuntimeSwitch("s37")
net.addHost("h37")
net.execScript("python controller.py s38 &", reboot=True)
net.addP4RuntimeSwitch("s38")
net.addHost("h38")
net.execScript("python controller.py s39 &", reboot=True)
net.addP4RuntimeSwitch("s39")
net.addHost("h39")
net.execScript("python controller.py s40 &", reboot=True)
net.addP4RuntimeSwitch("s40")
net.addHost("h40")
net.execScript("python controller.py s41 &", reboot=True)
net.addP4RuntimeSwitch("s41")
net.addHost("h41")
net.execScript("python controller.py s42 &", reboot=True)
net.addP4RuntimeSwitch("s42")
net.addHost("h42")
net.execScript("python controller.py s43 &", reboot=True)
net.addP4RuntimeSwitch("s43")
net.addHost("h43")
net.execScript("python controller.py s44 &", reboot=True)
net.addP4RuntimeSwitch("s44")
net.addHost("h44")
net.execScript("python controller.py s45 &", reboot=True)
net.addP4RuntimeSwitch("s45")
net.addHost("h45")
net.execScript("python controller.py s46 &", reboot=True)
net.addP4RuntimeSwitch("s46")
net.addHost("h46")
net.execScript("python controller.py s47 &", reboot=True)
net.addP4RuntimeSwitch("s47")
net.addHost("h47")
net.execScript("python controller.py s48 &", reboot=True)
net.addP4RuntimeSwitch("s48")
net.addHost("h48")
net.execScript("python controller.py s49 &", reboot=True)
net.addP4RuntimeSwitch("s49")
net.addHost("h49")
net.execScript("python controller.py s50 &", reboot=True)
net.addP4RuntimeSwitch("s50")
net.addHost("h50")
net.execScript("python controller.py s51 &", reboot=True)
net.addP4RuntimeSwitch("s51")
net.addHost("h51")
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
net.addLink("s12", "h12")
net.addLink("s13", "h13")
net.addLink("s14", "h14")
net.addLink("s15", "h15")
net.addLink("s16", "h16")
net.addLink("s17", "h17")
net.addLink("s18", "h18")
net.addLink("s19", "h19")
net.addLink("s20", "h20")
net.addLink("s21", "h21")
net.addLink("s22", "h22")
net.addLink("s23", "h23")
net.addLink("s24", "h24")
net.addLink("s25", "h25")
net.addLink("s26", "h26")
net.addLink("s27", "h27")
net.addLink("s28", "h28")
net.addLink("s29", "h29")
net.addLink("s30", "h30")
net.addLink("s31", "h31")
net.addLink("s32", "h32")
net.addLink("s33", "h33")
net.addLink("s34", "h34")
net.addLink("s35", "h35")
net.addLink("s36", "h36")
net.addLink("s37", "h37")
net.addLink("s38", "h38")
net.addLink("s39", "h39")
net.addLink("s40", "h40")
net.addLink("s41", "h41")
net.addLink("s42", "h42")
net.addLink("s43", "h43")
net.addLink("s44", "h44")
net.addLink("s45", "h45")
net.addLink("s46", "h46")
net.addLink("s47", "h47")
net.addLink("s48", "h48")
net.addLink("s49", "h49")
net.addLink("s50", "h50")
net.addLink("s51", "h51")

net.addLink("s1", "s49")
net.setDelay("s1", "s49", 219)
net.setBw("s1", "s49", 1)
net.addLink("s2", "s5")
net.setDelay("s2", "s5", 259)
net.setBw("s2", "s5", 1)
net.addLink("s3", "s43")
net.setDelay("s3", "s43", 177)
net.setBw("s3", "s43", 1)
net.addLink("s4", "s51")
net.setDelay("s4", "s51", 26)
net.setBw("s4", "s51", 1)
net.addLink("s5", "s36")
net.setDelay("s5", "s36", 135)
net.setBw("s5", "s36", 1)
net.addLink("s5", "s50")
net.setDelay("s5", "s50", 221)
net.setBw("s5", "s50", 1)
net.addLink("s6", "s47")
net.setDelay("s6", "s47", 232)
net.setBw("s6", "s47", 1)
net.addLink("s7", "s27")
net.setDelay("s7", "s27", 258)
net.setBw("s7", "s27", 1)
net.addLink("s7", "s32")
net.setDelay("s7", "s32", 257)
net.setBw("s7", "s32", 1)
net.addLink("s8", "s49")
net.setDelay("s8", "s49", 145)
net.setBw("s8", "s49", 1)
net.addLink("s9", "s47")
net.setDelay("s9", "s47", 146)
net.setBw("s9", "s47", 1)
net.addLink("s10", "s47")
net.setDelay("s10", "s47", 263)
net.setBw("s10", "s47", 1)
net.addLink("s11", "s16")
net.setDelay("s11", "s16", 259)
net.setBw("s11", "s16", 1)
net.addLink("s11", "s36")
net.setDelay("s11", "s36", 120)
net.setBw("s11", "s36", 1)
net.addLink("s11", "s47")
net.setDelay("s11", "s47", 84)
net.setBw("s11", "s47", 1)
net.addLink("s11", "s40")
net.setDelay("s11", "s40", 87)
net.setBw("s11", "s40", 1)
net.addLink("s12", "s36")
net.setDelay("s12", "s36", 184)
net.setBw("s12", "s36", 1)
net.addLink("s12", "s32")
net.setDelay("s12", "s32", 232)
net.setBw("s12", "s32", 1)
net.addLink("s13", "s36")
net.setDelay("s13", "s36", 262)
net.setBw("s13", "s36", 1)
net.addLink("s13", "s32")
net.setDelay("s13", "s32", 158)
net.setBw("s13", "s32", 1)
net.addLink("s14", "s16")
net.setDelay("s14", "s16", 293)
net.setBw("s14", "s16", 1)
net.addLink("s15", "s16")
net.setDelay("s15", "s16", 170)
net.setBw("s15", "s16", 1)
net.addLink("s16", "s17")
net.setDelay("s16", "s17", 148)
net.setBw("s16", "s17", 1)
net.addLink("s18", "s36")
net.setDelay("s18", "s36", 218)
net.setBw("s18", "s36", 1)
net.addLink("s18", "s32")
net.setDelay("s18", "s32", 59)
net.setBw("s18", "s32", 1)
net.addLink("s19", "s32")
net.setDelay("s19", "s32", 58)
net.setBw("s19", "s32", 1)
net.addLink("s20", "s21")
net.setDelay("s20", "s21", 33)
net.setBw("s20", "s21", 1)
net.addLink("s21", "s36")
net.setDelay("s21", "s36", 273)
net.setBw("s21", "s36", 1)
net.addLink("s21", "s22")
net.setDelay("s21", "s22", 203)
net.setBw("s21", "s22", 1)
net.addLink("s21", "s32")
net.setDelay("s21", "s32", 207)
net.setBw("s21", "s32", 1)
net.addLink("s23", "s26")
net.setDelay("s23", "s26", 208)
net.setBw("s23", "s26", 1)
net.addLink("s23", "s32")
net.setDelay("s23", "s32", 52)
net.setBw("s23", "s32", 1)
net.addLink("s24", "s27")
net.setDelay("s24", "s27", 215)
net.setBw("s24", "s27", 1)
net.addLink("s25", "s27")
net.setDelay("s25", "s27", 95)
net.setBw("s25", "s27", 1)
net.addLink("s26", "s36")
net.setDelay("s26", "s36", 39)
net.setBw("s26", "s36", 1)
net.addLink("s26", "s32")
net.setDelay("s26", "s32", 272)
net.setBw("s26", "s32", 1)
net.addLink("s27", "s36")
net.setDelay("s27", "s36", 200)
net.setBw("s27", "s36", 1)
net.addLink("s27", "s48")
net.setDelay("s27", "s48", 38)
net.setBw("s27", "s48", 1)
net.addLink("s28", "s36")
net.setDelay("s28", "s36", 63)
net.setBw("s28", "s36", 1)
net.addLink("s28", "s29")
net.setDelay("s28", "s29", 109)
net.setBw("s28", "s29", 1)
net.addLink("s28", "s30")
net.setDelay("s28", "s30", 114)
net.setBw("s28", "s30", 1)
net.addLink("s28", "s31")
net.setDelay("s28", "s31", 297)
net.setBw("s28", "s31", 1)
net.addLink("s28", "s32")
net.setDelay("s28", "s32", 84)
net.setBw("s28", "s32", 1)
net.addLink("s32", "s33")
net.setDelay("s32", "s33", 289)
net.setBw("s32", "s33", 1)
net.addLink("s32", "s35")
net.setDelay("s32", "s35", 269)
net.setBw("s32", "s35", 1)
net.addLink("s32", "s38")
net.setDelay("s32", "s38", 264)
net.setBw("s32", "s38", 1)
net.addLink("s32", "s40")
net.setDelay("s32", "s40", 293)
net.setBw("s32", "s40", 1)
net.addLink("s32", "s41")
net.setDelay("s32", "s41", 97)
net.setBw("s32", "s41", 1)
net.addLink("s32", "s44")
net.setDelay("s32", "s44", 124)
net.setBw("s32", "s44", 1)
net.addLink("s32", "s36")
net.setDelay("s32", "s36", 160)
net.setBw("s32", "s36", 1)
net.addLink("s32", "s50")
net.setDelay("s32", "s50", 245)
net.setBw("s32", "s50", 1)
net.addLink("s32", "s39")
net.setDelay("s32", "s39", 53)
net.setBw("s32", "s39", 1)
net.addLink("s34", "s41")
net.setDelay("s34", "s41", 29)
net.setBw("s34", "s41", 1)
net.addLink("s35", "s36")
net.setDelay("s35", "s36", 275)
net.setBw("s35", "s36", 1)
net.addLink("s36", "s41")
net.setDelay("s36", "s41", 173)
net.setBw("s36", "s41", 1)
net.addLink("s36", "s44")
net.setDelay("s36", "s44", 267)
net.setBw("s36", "s44", 1)
net.addLink("s36", "s45")
net.setDelay("s36", "s45", 189)
net.setBw("s36", "s45", 1)
net.addLink("s36", "s49")
net.setDelay("s36", "s49", 84)
net.setBw("s36", "s49", 1)
net.addLink("s36", "s50")
net.setDelay("s36", "s50", 263)
net.setBw("s36", "s50", 1)
net.addLink("s37", "s47")
net.setDelay("s37", "s47", 210)
net.setBw("s37", "s47", 1)
net.addLink("s39", "s45")
net.setDelay("s39", "s45", 111)
net.setBw("s39", "s45", 1)
net.addLink("s42", "s51")
net.setDelay("s42", "s51", 125)
net.setBw("s42", "s51", 1)
net.addLink("s43", "s51")
net.setDelay("s43", "s51", 42)
net.setBw("s43", "s51", 1)
net.addLink("s45", "s46")
net.setDelay("s45", "s46", 126)
net.setBw("s45", "s46", 1)
net.addLink("s49", "s50")
net.setDelay("s49", "s50", 299)
net.setBw("s49", "s50", 1)
net.addLink("s50", "s51")
net.setDelay("s50", "s51", 48)
net.setBw("s50", "s51", 1)
# Assignment strategy
net.mixed()
# Nodes general options
net.enableCpuPortAll()
net.enablePcapDumpAll()
net.enableLogAll()
net.enableCli()
net.startNetwork()
