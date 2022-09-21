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
net.execScript("python controller.py s3 &", reboot=True)
net.addP4RuntimeSwitch("s3")
net.execScript("python controller.py s4 &", reboot=True)
net.addP4RuntimeSwitch("s4")
net.execScript("python controller.py s5 &", reboot=True)
net.addP4RuntimeSwitch("s5")
net.addHost("h5")
net.execScript("python controller.py s6 &", reboot=True)
net.addP4RuntimeSwitch("s6")
net.execScript("python controller.py s7 &", reboot=True)
net.addP4RuntimeSwitch("s7")
net.execScript("python controller.py s8 &", reboot=True)
net.addP4RuntimeSwitch("s8")
net.execScript("python controller.py s9 &", reboot=True)
net.addP4RuntimeSwitch("s9")
net.addHost("h9")
net.execScript("python controller.py s10 &", reboot=True)
net.addP4RuntimeSwitch("s10")
net.execScript("python controller.py s11 &", reboot=True)
net.addP4RuntimeSwitch("s11")
net.execScript("python controller.py s12 &", reboot=True)
net.addP4RuntimeSwitch("s12")
net.execScript("python controller.py s13 &", reboot=True)
net.addP4RuntimeSwitch("s13")
net.addHost("h13")
net.execScript("python controller.py s14 &", reboot=True)
net.addP4RuntimeSwitch("s14")
net.execScript("python controller.py s15 &", reboot=True)
net.addP4RuntimeSwitch("s15")
net.execScript("python controller.py s16 &", reboot=True)
net.addP4RuntimeSwitch("s16")
net.execScript("python controller.py s17 &", reboot=True)
net.addP4RuntimeSwitch("s17")
net.addHost("h17")
net.execScript("python controller.py s18 &", reboot=True)
net.addP4RuntimeSwitch("s18")
net.execScript("python controller.py s19 &", reboot=True)
net.addP4RuntimeSwitch("s19")
net.execScript("python controller.py s20 &", reboot=True)
net.addP4RuntimeSwitch("s20")
net.execScript("python controller.py s21 &", reboot=True)
net.addP4RuntimeSwitch("s21")
net.addHost("h21")
net.execScript("python controller.py s22 &", reboot=True)
net.addP4RuntimeSwitch("s22")
net.execScript("python controller.py s23 &", reboot=True)
net.addP4RuntimeSwitch("s23")
net.execScript("python controller.py s24 &", reboot=True)
net.addP4RuntimeSwitch("s24")
net.execScript("python controller.py s25 &", reboot=True)
net.addP4RuntimeSwitch("s25")
net.addHost("h25")
net.execScript("python controller.py s26 &", reboot=True)
net.addP4RuntimeSwitch("s26")
net.execScript("python controller.py s27 &", reboot=True)
net.addP4RuntimeSwitch("s27")
net.execScript("python controller.py s28 &", reboot=True)
net.addP4RuntimeSwitch("s28")
net.execScript("python controller.py s29 &", reboot=True)
net.addP4RuntimeSwitch("s29")
net.addHost("h29")
net.execScript("python controller.py s30 &", reboot=True)
net.addP4RuntimeSwitch("s30")
net.execScript("python controller.py s31 &", reboot=True)
net.addP4RuntimeSwitch("s31")
net.execScript("python controller.py s32 &", reboot=True)
net.addP4RuntimeSwitch("s32")
net.execScript("python controller.py s33 &", reboot=True)
net.addP4RuntimeSwitch("s33")
net.addHost("h33")
net.execScript("python controller.py s34 &", reboot=True)
net.addP4RuntimeSwitch("s34")
net.execScript("python controller.py s35 &", reboot=True)
net.addP4RuntimeSwitch("s35")
net.execScript("python controller.py s36 &", reboot=True)
net.addP4RuntimeSwitch("s36")
net.execScript("python controller.py s37 &", reboot=True)
net.addP4RuntimeSwitch("s37")
net.addHost("h37")
net.execScript("python controller.py s38 &", reboot=True)
net.addP4RuntimeSwitch("s38")
net.execScript("python controller.py s39 &", reboot=True)
net.addP4RuntimeSwitch("s39")
net.execScript("python controller.py s40 &", reboot=True)
net.addP4RuntimeSwitch("s40")
net.execScript("python controller.py s41 &", reboot=True)
net.addP4RuntimeSwitch("s41")
net.addHost("h41")
net.execScript("python controller.py s42 &", reboot=True)
net.addP4RuntimeSwitch("s42")
net.execScript("python controller.py s43 &", reboot=True)
net.addP4RuntimeSwitch("s43")
net.execScript("python controller.py s44 &", reboot=True)
net.addP4RuntimeSwitch("s44")
net.execScript("python controller.py s45 &", reboot=True)
net.addP4RuntimeSwitch("s45")
net.addHost("h45")
net.execScript("python controller.py s46 &", reboot=True)
net.addP4RuntimeSwitch("s46")
net.execScript("python controller.py s47 &", reboot=True)
net.addP4RuntimeSwitch("s47")
net.execScript("python controller.py s48 &", reboot=True)
net.addP4RuntimeSwitch("s48")
net.execScript("python controller.py s49 &", reboot=True)
net.addP4RuntimeSwitch("s49")
net.addHost("h49")
net.execScript("python controller.py s50 &", reboot=True)
net.addP4RuntimeSwitch("s50")
net.execScript("python controller.py s51 &", reboot=True)
net.addP4RuntimeSwitch("s51")
net.execScript("python controller.py s52 &", reboot=True)
net.addP4RuntimeSwitch("s52")
net.execScript("python controller.py s53 &", reboot=True)
net.addP4RuntimeSwitch("s53")
net.addHost("h53")
net.execScript("python controller.py s54 &", reboot=True)
net.addP4RuntimeSwitch("s54")
net.execScript("python controller.py s55 &", reboot=True)
net.addP4RuntimeSwitch("s55")
net.execScript("python controller.py s56 &", reboot=True)
net.addP4RuntimeSwitch("s56")
net.execScript("python controller.py s57 &", reboot=True)
net.addP4RuntimeSwitch("s57")
net.addHost("h57")
net.execScript("python controller.py s58 &", reboot=True)
net.addP4RuntimeSwitch("s58")
net.execScript("python controller.py s59 &", reboot=True)
net.addP4RuntimeSwitch("s59")
net.execScript("python controller.py s60 &", reboot=True)
net.addP4RuntimeSwitch("s60")
net.execScript("python controller.py s61 &", reboot=True)
net.addP4RuntimeSwitch("s61")
net.addHost("h61")
net.execScript("python controller.py s62 &", reboot=True)
net.addP4RuntimeSwitch("s62")
net.execScript("python controller.py s63 &", reboot=True)
net.addP4RuntimeSwitch("s63")
net.execScript("python controller.py s64 &", reboot=True)
net.addP4RuntimeSwitch("s64")
net.execScript("python controller.py s65 &", reboot=True)
net.addP4RuntimeSwitch("s65")
net.addHost("h65")
net.execScript("python controller.py s66 &", reboot=True)
net.addP4RuntimeSwitch("s66")
net.execScript("python controller.py s67 &", reboot=True)
net.addP4RuntimeSwitch("s67")
net.execScript("python controller.py s68 &", reboot=True)
net.addP4RuntimeSwitch("s68")
net.execScript("python controller.py s69 &", reboot=True)
net.addP4RuntimeSwitch("s69")
net.addHost("h69")
net.execScript("python controller.py s70 &", reboot=True)
net.addP4RuntimeSwitch("s70")
net.execScript("python controller.py s71 &", reboot=True)
net.addP4RuntimeSwitch("s71")
net.execScript("python controller.py s72 &", reboot=True)
net.addP4RuntimeSwitch("s72")
net.execScript("python controller.py s73 &", reboot=True)
net.addP4RuntimeSwitch("s73")
net.addHost("h73")
net.execScript("python controller.py s74 &", reboot=True)
net.addP4RuntimeSwitch("s74")
net.execScript("python controller.py s75 &", reboot=True)
net.addP4RuntimeSwitch("s75")
net.execScript("python controller.py s76 &", reboot=True)
net.addP4RuntimeSwitch("s76")
net.execScript("python controller.py s77 &", reboot=True)
net.addP4RuntimeSwitch("s77")
net.addHost("h77")
net.execScript("python controller.py s78 &", reboot=True)
net.addP4RuntimeSwitch("s78")
net.execScript("python controller.py s79 &", reboot=True)
net.addP4RuntimeSwitch("s79")
net.execScript("python controller.py s80 &", reboot=True)
net.addP4RuntimeSwitch("s80")
net.execScript("python controller.py s81 &", reboot=True)
net.addP4RuntimeSwitch("s81")
net.addHost("h81")
net.execScript("python controller.py s82 &", reboot=True)
net.addP4RuntimeSwitch("s82")
net.execScript("python controller.py s83 &", reboot=True)
net.addP4RuntimeSwitch("s83")
net.execScript("python controller.py s84 &", reboot=True)
net.addP4RuntimeSwitch("s84")
net.execScript("python controller.py s85 &", reboot=True)
net.addP4RuntimeSwitch("s85")
net.addHost("h85")
net.execScript("python controller.py s86 &", reboot=True)
net.addP4RuntimeSwitch("s86")
net.execScript("python controller.py s87 &", reboot=True)
net.addP4RuntimeSwitch("s87")
net.execScript("python controller.py s88 &", reboot=True)
net.addP4RuntimeSwitch("s88")
net.execScript("python controller.py s89 &", reboot=True)
net.addP4RuntimeSwitch("s89")
net.addHost("h89")
net.execScript("python controller.py s90 &", reboot=True)
net.addP4RuntimeSwitch("s90")
net.execScript("python controller.py s91 &", reboot=True)
net.addP4RuntimeSwitch("s91")
net.execScript("python controller.py s92 &", reboot=True)
net.addP4RuntimeSwitch("s92")
net.execScript("python controller.py s93 &", reboot=True)
net.addP4RuntimeSwitch("s93")
net.addHost("h93")
net.execScript("python controller.py s94 &", reboot=True)
net.addP4RuntimeSwitch("s94")
net.execScript("python controller.py s95 &", reboot=True)
net.addP4RuntimeSwitch("s95")
net.execScript("python controller.py s96 &", reboot=True)
net.addP4RuntimeSwitch("s96")
net.execScript("python controller.py s97 &", reboot=True)
net.addP4RuntimeSwitch("s97")
net.addHost("h97")
net.execScript("python controller.py s98 &", reboot=True)
net.addP4RuntimeSwitch("s98")
net.execScript("python controller.py s99 &", reboot=True)
net.addP4RuntimeSwitch("s99")
net.execScript("python controller.py s100 &", reboot=True)
net.addP4RuntimeSwitch("s100")
net.execScript("python controller.py s101 &", reboot=True)
net.addP4RuntimeSwitch("s101")
net.addHost("h101")
net.execScript("python controller.py s102 &", reboot=True)
net.addP4RuntimeSwitch("s102")
net.execScript("python controller.py s103 &", reboot=True)
net.addP4RuntimeSwitch("s103")
net.execScript("python controller.py s104 &", reboot=True)
net.addP4RuntimeSwitch("s104")
net.execScript("python controller.py s105 &", reboot=True)
net.addP4RuntimeSwitch("s105")
net.addHost("h105")
net.execScript("python controller.py s106 &", reboot=True)
net.addP4RuntimeSwitch("s106")
net.execScript("python controller.py s107 &", reboot=True)
net.addP4RuntimeSwitch("s107")
net.execScript("python controller.py s108 &", reboot=True)
net.addP4RuntimeSwitch("s108")
net.execScript("python controller.py s109 &", reboot=True)
net.addP4RuntimeSwitch("s109")
net.addHost("h109")
net.execScript("python controller.py s110 &", reboot=True)
net.addP4RuntimeSwitch("s110")
net.execScript("python controller.py s111 &", reboot=True)
net.addP4RuntimeSwitch("s111")
net.execScript("python controller.py s112 &", reboot=True)
net.addP4RuntimeSwitch("s112")
net.execScript("python controller.py s113 &", reboot=True)
net.addP4RuntimeSwitch("s113")
net.addHost("h113")
net.execScript("python controller.py s114 &", reboot=True)
net.addP4RuntimeSwitch("s114")
net.execScript("python controller.py s115 &", reboot=True)
net.addP4RuntimeSwitch("s115")
net.execScript("python controller.py s116 &", reboot=True)
net.addP4RuntimeSwitch("s116")
net.execScript("python controller.py s117 &", reboot=True)
net.addP4RuntimeSwitch("s117")
net.addHost("h117")
net.execScript("python controller.py s118 &", reboot=True)
net.addP4RuntimeSwitch("s118")
net.execScript("python controller.py s119 &", reboot=True)
net.addP4RuntimeSwitch("s119")
net.execScript("python controller.py s120 &", reboot=True)
net.addP4RuntimeSwitch("s120")
net.execScript("python controller.py s121 &", reboot=True)
net.addP4RuntimeSwitch("s121")
net.addHost("h121")
net.execScript("python controller.py s122 &", reboot=True)
net.addP4RuntimeSwitch("s122")
net.execScript("python controller.py s123 &", reboot=True)
net.addP4RuntimeSwitch("s123")
net.execScript("python controller.py s124 &", reboot=True)
net.addP4RuntimeSwitch("s124")
net.execScript("python controller.py s125 &", reboot=True)
net.addP4RuntimeSwitch("s125")
net.addHost("h125")
net.execScript("python controller.py s126 &", reboot=True)
net.addP4RuntimeSwitch("s126")
net.execScript("python controller.py s127 &", reboot=True)
net.addP4RuntimeSwitch("s127")
net.execScript("python controller.py s128 &", reboot=True)
net.addP4RuntimeSwitch("s128")
net.execScript("python controller.py s129 &", reboot=True)
net.addP4RuntimeSwitch("s129")
net.addHost("h129")
net.execScript("python controller.py s130 &", reboot=True)
net.addP4RuntimeSwitch("s130")
net.execScript("python controller.py s131 &", reboot=True)
net.addP4RuntimeSwitch("s131")
net.execScript("python controller.py s132 &", reboot=True)
net.addP4RuntimeSwitch("s132")
net.execScript("python controller.py s133 &", reboot=True)
net.addP4RuntimeSwitch("s133")
net.addHost("h133")
net.execScript("python controller.py s134 &", reboot=True)
net.addP4RuntimeSwitch("s134")
net.execScript("python controller.py s135 &", reboot=True)
net.addP4RuntimeSwitch("s135")
net.execScript("python controller.py s136 &", reboot=True)
net.addP4RuntimeSwitch("s136")
net.execScript("python controller.py s137 &", reboot=True)
net.addP4RuntimeSwitch("s137")
net.addHost("h137")
net.execScript("python controller.py s138 &", reboot=True)
net.addP4RuntimeSwitch("s138")
net.execScript("python controller.py s139 &", reboot=True)
net.addP4RuntimeSwitch("s139")
net.execScript("python controller.py s140 &", reboot=True)
net.addP4RuntimeSwitch("s140")
net.execScript("python controller.py s141 &", reboot=True)
net.addP4RuntimeSwitch("s141")
net.addHost("h141")
net.execScript("python controller.py s142 &", reboot=True)
net.addP4RuntimeSwitch("s142")
net.execScript("python controller.py s143 &", reboot=True)
net.addP4RuntimeSwitch("s143")
net.execScript("python controller.py s144 &", reboot=True)
net.addP4RuntimeSwitch("s144")
net.execScript("python controller.py s145 &", reboot=True)
net.addP4RuntimeSwitch("s145")
net.addHost("h145")
net.execScript("python controller.py s146 &", reboot=True)
net.addP4RuntimeSwitch("s146")
net.execScript("python controller.py s147 &", reboot=True)
net.addP4RuntimeSwitch("s147")
net.execScript("python controller.py s148 &", reboot=True)
net.addP4RuntimeSwitch("s148")
net.execScript("python controller.py s149 &", reboot=True)
net.addP4RuntimeSwitch("s149")
net.addHost("h149")
net.setP4SourceAll("./p4src/main.p4")

net.addLink("s1", "h1")

net.addLink("s1", "s15")
net.setDelay("s1", "s15", 112)
net.setBw("s1", "s15", 10)
net.addLink("s2", "s18")
net.setDelay("s2", "s18", 117)
net.setBw("s2", "s18", 10)
net.addLink("s3", "s129")
net.setDelay("s3", "s129", 120)
net.setBw("s3", "s129", 10)
net.addLink("s3", "s4")
net.setDelay("s3", "s4", 110)
net.setBw("s3", "s4", 10)
net.addLink("s4", "s126")
net.setDelay("s4", "s126", 115)
net.setBw("s4", "s126", 10)
net.addLink("s5", "s17")
net.setDelay("s5", "s17", 114)
net.setBw("s5", "s17", 10)
net.addLink("s5", "s6")
net.setDelay("s5", "s6", 109)
net.setBw("s5", "s6", 10)
net.addLink("s6", "s7")
net.setDelay("s6", "s7", 113)
net.setBw("s6", "s7", 10)
net.addLink("s7", "s8")
net.setDelay("s7", "s8", 119)
net.setBw("s7", "s8", 10)
net.addLink("s8", "s9")
net.setDelay("s8", "s9", 121)
net.setBw("s8", "s9", 10)
net.addLink("s9", "s10")
net.setDelay("s9", "s10", 121)
net.setBw("s9", "s10", 10)
net.addLink("s10", "s15")
net.setDelay("s10", "s15", 131)
net.setBw("s10", "s15", 10)
net.addLink("s11", "s17")
net.setDelay("s11", "s17", 131)
net.setBw("s11", "s17", 10)
net.addLink("s11", "s47")
net.setDelay("s11", "s47", 124)
net.setBw("s11", "s47", 10)
net.addLink("s12", "s99")
net.setDelay("s12", "s99", 112)
net.setBw("s12", "s99", 10)
net.addLink("s12", "s101")
net.setDelay("s12", "s101", 120)
net.setBw("s12", "s101", 10)
net.addLink("s12", "s96")
net.setDelay("s12", "s96", 124)
net.setBw("s12", "s96", 10)
net.addLink("s13", "s118")
net.setDelay("s13", "s118", 124)
net.setBw("s13", "s118", 10)
net.addLink("s14", "s148")
net.setDelay("s14", "s148", 110)
net.setBw("s14", "s148", 10)
net.addLink("s15", "s95")
net.setDelay("s15", "s95", 132)
net.setBw("s15", "s95", 10)
net.addLink("s16", "s132")
net.setDelay("s16", "s132", 108)
net.setBw("s16", "s132", 10)
net.addLink("s16", "s126")
net.setDelay("s16", "s126", 116)
net.setBw("s16", "s126", 10)
net.addLink("s17", "s96")
net.setDelay("s17", "s96", 118)
net.setBw("s17", "s96", 10)
net.addLink("s18", "s133")
net.setDelay("s18", "s133", 112)
net.setBw("s18", "s133", 10)
net.addLink("s18", "s95")
net.setDelay("s18", "s95", 113)
net.setBw("s18", "s95", 10)
net.addLink("s19", "s42")
net.setDelay("s19", "s42", 113)
net.setBw("s19", "s42", 10)
net.addLink("s19", "s104")
net.setDelay("s19", "s104", 125)
net.setBw("s19", "s104", 10)
net.addLink("s20", "s60")
net.setDelay("s20", "s60", 129)
net.setBw("s20", "s60", 10)
net.addLink("s20", "s143")
net.setDelay("s20", "s143", 132)
net.setBw("s20", "s143", 10)
net.addLink("s21", "s81")
net.setDelay("s21", "s81", 112)
net.setBw("s21", "s81", 10)
net.addLink("s21", "s134")
net.setDelay("s21", "s134", 111)
net.setBw("s21", "s134", 10)
net.addLink("s21", "s135")
net.setDelay("s21", "s135", 111)
net.setBw("s21", "s135", 10)
net.addLink("s21", "s142")
net.setDelay("s21", "s142", 111)
net.setBw("s21", "s142", 10)
net.addLink("s21", "s145")
net.setDelay("s21", "s145", 119)
net.setBw("s21", "s145", 10)
net.addLink("s21", "s82")
net.setDelay("s21", "s82", 129)
net.setBw("s21", "s82", 10)
net.addLink("s22", "s27")
net.setDelay("s22", "s27", 130)
net.setBw("s22", "s27", 10)
net.addLink("s22", "s24")
net.setDelay("s22", "s24", 116)
net.setBw("s22", "s24", 10)
net.addLink("s23", "s143")
net.setDelay("s23", "s143", 118)
net.setBw("s23", "s143", 10)
net.addLink("s23", "s24")
net.setDelay("s23", "s24", 123)
net.setBw("s23", "s24", 10)
net.addLink("s25", "s82")
net.setDelay("s25", "s82", 124)
net.setBw("s25", "s82", 10)
net.addLink("s25", "s28")
net.setDelay("s25", "s28", 112)
net.setBw("s25", "s28", 10)
net.addLink("s25", "s26")
net.setDelay("s25", "s26", 131)
net.setBw("s25", "s26", 10)
net.addLink("s26", "s90")
net.setDelay("s26", "s90", 121)
net.setBw("s26", "s90", 10)
net.addLink("s26", "s51")
net.setDelay("s26", "s51", 109)
net.setBw("s26", "s51", 10)
net.addLink("s27", "s28")
net.setDelay("s27", "s28", 115)
net.setBw("s27", "s28", 10)
net.addLink("s28", "s145")
net.setDelay("s28", "s145", 127)
net.setBw("s28", "s145", 10)
net.addLink("s29", "s143")
net.setDelay("s29", "s143", 129)
net.setBw("s29", "s143", 10)
net.addLink("s29", "s55")
net.setDelay("s29", "s55", 113)
net.setBw("s29", "s55", 10)
net.addLink("s30", "s52")
net.setDelay("s30", "s52", 132)
net.setBw("s30", "s52", 10)
net.addLink("s30", "s140")
net.setDelay("s30", "s140", 130)
net.setBw("s30", "s140", 10)
net.addLink("s30", "s143")
net.setDelay("s30", "s143", 130)
net.setBw("s30", "s143", 10)
net.addLink("s31", "s127")
net.setDelay("s31", "s127", 120)
net.setBw("s31", "s127", 10)
net.addLink("s32", "s73")
net.setDelay("s32", "s73", 121)
net.setBw("s32", "s73", 10)
net.addLink("s32", "s63")
net.setDelay("s32", "s63", 119)
net.setBw("s32", "s63", 10)
net.addLink("s33", "s130")
net.setDelay("s33", "s130", 119)
net.setBw("s33", "s130", 10)
net.addLink("s33", "s36")
net.setDelay("s33", "s36", 120)
net.setBw("s33", "s36", 10)
net.addLink("s34", "s130")
net.setDelay("s34", "s130", 108)
net.setBw("s34", "s130", 10)
net.addLink("s34", "s62")
net.setDelay("s34", "s62", 131)
net.setBw("s34", "s62", 10)
net.addLink("s35", "s73")
net.setDelay("s35", "s73", 126)
net.setBw("s35", "s73", 10)
net.addLink("s35", "s74")
net.setDelay("s35", "s74", 122)
net.setBw("s35", "s74", 10)
net.addLink("s36", "s74")
net.setDelay("s36", "s74", 122)
net.setBw("s36", "s74", 10)
net.addLink("s37", "s76")
net.setDelay("s37", "s76", 121)
net.setBw("s37", "s76", 10)
net.addLink("s37", "s40")
net.setDelay("s37", "s40", 126)
net.setBw("s37", "s40", 10)
net.addLink("s38", "s123")
net.setDelay("s38", "s123", 110)
net.setBw("s38", "s123", 10)
net.addLink("s38", "s76")
net.setDelay("s38", "s76", 113)
net.setBw("s38", "s76", 10)
net.addLink("s39", "s77")
net.setDelay("s39", "s77", 125)
net.setBw("s39", "s77", 10)
net.addLink("s39", "s78")
net.setDelay("s39", "s78", 121)
net.setBw("s39", "s78", 10)
net.addLink("s40", "s71")
net.setDelay("s40", "s71", 108)
net.setBw("s40", "s71", 10)
net.addLink("s41", "s65")
net.setDelay("s41", "s65", 116)
net.setBw("s41", "s65", 10)
net.addLink("s41", "s66")
net.setDelay("s41", "s66", 110)
net.setBw("s41", "s66", 10)
net.addLink("s41", "s67")
net.setDelay("s41", "s67", 116)
net.setBw("s41", "s67", 10)
net.addLink("s41", "s64")
net.setDelay("s41", "s64", 128)
net.setBw("s41", "s64", 10)
net.addLink("s42", "s99")
net.setDelay("s42", "s99", 128)
net.setBw("s42", "s99", 10)
net.addLink("s42", "s102")
net.setDelay("s42", "s102", 122)
net.setBw("s42", "s102", 10)
net.addLink("s42", "s105")
net.setDelay("s42", "s105", 127)
net.setBw("s42", "s105", 10)
net.addLink("s42", "s106")
net.setDelay("s42", "s106", 130)
net.setBw("s42", "s106", 10)
net.addLink("s42", "s107")
net.setDelay("s42", "s107", 109)
net.setBw("s42", "s107", 10)
net.addLink("s42", "s45")
net.setDelay("s42", "s45", 116)
net.setBw("s42", "s45", 10)
net.addLink("s42", "s48")
net.setDelay("s42", "s48", 128)
net.setBw("s42", "s48", 10)
net.addLink("s43", "s44")
net.setDelay("s43", "s44", 121)
net.setBw("s43", "s44", 10)
net.addLink("s43", "s149")
net.setDelay("s43", "s149", 111)
net.setBw("s43", "s149", 10)
net.addLink("s44", "s138")
net.setDelay("s44", "s138", 120)
net.setBw("s44", "s138", 10)
net.addLink("s45", "s49")
net.setDelay("s45", "s49", 108)
net.setBw("s45", "s49", 10)
net.addLink("s45", "s46")
net.setDelay("s45", "s46", 116)
net.setBw("s45", "s46", 10)
net.addLink("s46", "s49")
net.setDelay("s46", "s49", 129)
net.setBw("s46", "s49", 10)
net.addLink("s46", "s129")
net.setDelay("s46", "s129", 120)
net.setBw("s46", "s129", 10)
net.addLink("s50", "s129")
net.setDelay("s50", "s129", 111)
net.setBw("s50", "s129", 10)
net.addLink("s50", "s128")
net.setDelay("s50", "s128", 131)
net.setBw("s50", "s128", 10)
net.addLink("s51", "s58")
net.setDelay("s51", "s58", 116)
net.setBw("s51", "s58", 10)
net.addLink("s52", "s118")
net.setDelay("s52", "s118", 111)
net.setBw("s52", "s118", 10)
net.addLink("s52", "s141")
net.setDelay("s52", "s141", 132)
net.setBw("s52", "s141", 10)
net.addLink("s52", "s88")
net.setDelay("s52", "s88", 122)
net.setBw("s52", "s88", 10)
net.addLink("s53", "s144")
net.setDelay("s53", "s144", 124)
net.setBw("s53", "s144", 10)
net.addLink("s53", "s54")
net.setDelay("s53", "s54", 109)
net.setBw("s53", "s54", 10)
net.addLink("s53", "s56")
net.setDelay("s53", "s56", 109)
net.setBw("s53", "s56", 10)
net.addLink("s54", "s59")
net.setDelay("s54", "s59", 120)
net.setBw("s54", "s59", 10)
net.addLink("s55", "s56")
net.setDelay("s55", "s56", 112)
net.setBw("s55", "s56", 10)
net.addLink("s57", "s58")
net.setDelay("s57", "s58", 108)
net.setBw("s57", "s58", 10)
net.addLink("s57", "s60")
net.setDelay("s57", "s60", 127)
net.setBw("s57", "s60", 10)
net.addLink("s59", "s143")
net.setDelay("s59", "s143", 117)
net.setBw("s59", "s143", 10)
net.addLink("s59", "s118")
net.setDelay("s59", "s118", 130)
net.setBw("s59", "s118", 10)
net.addLink("s61", "s131")
net.setDelay("s61", "s131", 132)
net.setBw("s61", "s131", 10)
net.addLink("s62", "s131")
net.setDelay("s62", "s131", 115)
net.setBw("s62", "s131", 10)
net.addLink("s62", "s63")
net.setDelay("s62", "s63", 124)
net.setBw("s62", "s63", 10)
net.addLink("s63", "s132")
net.setDelay("s63", "s132", 118)
net.setBw("s63", "s132", 10)
net.addLink("s65", "s66")
net.setDelay("s65", "s66", 117)
net.setBw("s65", "s66", 10)
net.addLink("s65", "s127")
net.setDelay("s65", "s127", 120)
net.setBw("s65", "s127", 10)
net.addLink("s67", "s103")
net.setDelay("s67", "s103", 112)
net.setBw("s67", "s103", 10)
net.addLink("s68", "s108")
net.setDelay("s68", "s108", 114)
net.setBw("s68", "s108", 10)
net.addLink("s68", "s103")
net.setDelay("s68", "s103", 118)
net.setBw("s68", "s103", 10)
net.addLink("s69", "s131")
net.setDelay("s69", "s131", 108)
net.setBw("s69", "s131", 10)
net.addLink("s69", "s84")
net.setDelay("s69", "s84", 114)
net.setBw("s69", "s84", 10)
net.addLink("s70", "s131")
net.setDelay("s70", "s131", 130)
net.setBw("s70", "s131", 10)
net.addLink("s71", "s121")
net.setDelay("s71", "s121", 121)
net.setBw("s71", "s121", 10)
net.addLink("s71", "s126")
net.setDelay("s71", "s126", 113)
net.setBw("s71", "s126", 10)
net.addLink("s71", "s119")
net.setDelay("s71", "s119", 109)
net.setBw("s71", "s119", 10)
net.addLink("s71", "s78")
net.setDelay("s71", "s78", 127)
net.setBw("s71", "s78", 10)
net.addLink("s72", "s89")
net.setDelay("s72", "s89", 124)
net.setBw("s72", "s89", 10)
net.addLink("s72", "s130")
net.setDelay("s72", "s130", 122)
net.setBw("s72", "s130", 10)
net.addLink("s73", "s124")
net.setDelay("s73", "s124", 109)
net.setBw("s73", "s124", 10)
net.addLink("s75", "s113")
net.setDelay("s75", "s113", 132)
net.setBw("s75", "s113", 10)
net.addLink("s75", "s146")
net.setDelay("s75", "s146", 126)
net.setBw("s75", "s146", 10)
net.addLink("s77", "s123")
net.setDelay("s77", "s123", 123)
net.setBw("s77", "s123", 10)
net.addLink("s78", "s117")
net.setDelay("s78", "s117", 125)
net.setBw("s78", "s117", 10)
net.addLink("s79", "s130")
net.setDelay("s79", "s130", 117)
net.setBw("s79", "s130", 10)
net.addLink("s79", "s86")
net.setDelay("s79", "s86", 123)
net.setBw("s79", "s86", 10)
net.addLink("s80", "s81")
net.setDelay("s80", "s81", 125)
net.setBw("s80", "s81", 10)
net.addLink("s80", "s82")
net.setDelay("s80", "s82", 131)
net.setBw("s80", "s82", 10)
net.addLink("s80", "s87")
net.setDelay("s80", "s87", 108)
net.setBw("s80", "s87", 10)
net.addLink("s82", "s83")
net.setDelay("s82", "s83", 121)
net.setBw("s82", "s83", 10)
net.addLink("s83", "s86")
net.setDelay("s83", "s86", 132)
net.setBw("s83", "s86", 10)
net.addLink("s84", "s131")
net.setDelay("s84", "s131", 114)
net.setBw("s84", "s131", 10)
net.addLink("s84", "s85")
net.setDelay("s84", "s85", 116)
net.setBw("s84", "s85", 10)
net.addLink("s85", "s131")
net.setDelay("s85", "s131", 117)
net.setBw("s85", "s131", 10)
net.addLink("s87", "s130")
net.setDelay("s87", "s130", 130)
net.setBw("s87", "s130", 10)
net.addLink("s88", "s113")
net.setDelay("s88", "s113", 108)
net.setBw("s88", "s113", 10)
net.addLink("s88", "s146")
net.setDelay("s88", "s146", 121)
net.setBw("s88", "s146", 10)
net.addLink("s88", "s118")
net.setDelay("s88", "s118", 108)
net.setBw("s88", "s118", 10)
net.addLink("s89", "s90")
net.setDelay("s89", "s90", 112)
net.setBw("s89", "s90", 10)
net.addLink("s91", "s141")
net.setDelay("s91", "s141", 130)
net.setBw("s91", "s141", 10)
net.addLink("s91", "s112")
net.setDelay("s91", "s112", 122)
net.setBw("s91", "s112", 10)
net.addLink("s92", "s93")
net.setDelay("s92", "s93", 114)
net.setBw("s92", "s93", 10)
net.addLink("s92", "s110")
net.setDelay("s92", "s110", 130)
net.setBw("s92", "s110", 10)
net.addLink("s93", "s95")
net.setDelay("s93", "s95", 118)
net.setBw("s93", "s95", 10)
net.addLink("s94", "s97")
net.setDelay("s94", "s97", 131)
net.setBw("s94", "s97", 10)
net.addLink("s94", "s101")
net.setDelay("s94", "s101", 116)
net.setBw("s94", "s101", 10)
net.addLink("s94", "s95")
net.setDelay("s94", "s95", 115)
net.setBw("s94", "s95", 10)
net.addLink("s95", "s100")
net.setDelay("s95", "s100", 114)
net.setBw("s95", "s100", 10)
net.addLink("s96", "s97")
net.setDelay("s96", "s97", 114)
net.setBw("s96", "s97", 10)
net.addLink("s98", "s101")
net.setDelay("s98", "s101", 108)
net.setBw("s98", "s101", 10)
net.addLink("s98", "s104")
net.setDelay("s98", "s104", 121)
net.setBw("s98", "s104", 10)
net.addLink("s100", "s104")
net.setDelay("s100", "s104", 113)
net.setBw("s100", "s104", 10)
net.addLink("s102", "s103")
net.setDelay("s102", "s103", 123)
net.setBw("s102", "s103", 10)
net.addLink("s104", "s107")
net.setDelay("s104", "s107", 115)
net.setBw("s104", "s107", 10)
net.addLink("s106", "s109")
net.setDelay("s106", "s109", 123)
net.setBw("s106", "s109", 10)
net.addLink("s108", "s109")
net.setDelay("s108", "s109", 125)
net.setBw("s108", "s109", 10)
net.addLink("s108", "s111")
net.setDelay("s108", "s111", 117)
net.setBw("s108", "s111", 10)
net.addLink("s110", "s111")
net.setDelay("s110", "s111", 110)
net.setBw("s110", "s111", 10)
net.addLink("s111", "s122")
net.setDelay("s111", "s122", 124)
net.setBw("s111", "s122", 10)
net.addLink("s112", "s113")
net.setDelay("s112", "s113", 124)
net.setBw("s112", "s113", 10)
net.addLink("s113", "s146")
net.setDelay("s113", "s146", 114)
net.setBw("s113", "s146", 10)
net.addLink("s113", "s136")
net.setDelay("s113", "s136", 110)
net.setBw("s113", "s136", 10)
net.addLink("s114", "s121")
net.setDelay("s114", "s121", 108)
net.setBw("s114", "s121", 10)
net.addLink("s114", "s117")
net.setDelay("s114", "s117", 125)
net.setBw("s114", "s117", 10)
net.addLink("s115", "s121")
net.setDelay("s115", "s121", 121)
net.setBw("s115", "s121", 10)
net.addLink("s115", "s131")
net.setDelay("s115", "s131", 132)
net.setBw("s115", "s131", 10)
net.addLink("s115", "s116")
net.setDelay("s115", "s116", 113)
net.setBw("s115", "s116", 10)
net.addLink("s116", "s117")
net.setDelay("s116", "s117", 111)
net.setBw("s116", "s117", 10)
net.addLink("s117", "s122")
net.setDelay("s117", "s122", 111)
net.setBw("s117", "s122", 10)
net.addLink("s119", "s120")
net.setDelay("s119", "s120", 132)
net.setBw("s119", "s120", 10)
net.addLink("s120", "s121")
net.setDelay("s120", "s121", 117)
net.setBw("s120", "s121", 10)
net.addLink("s121", "s131")
net.setDelay("s121", "s131", 115)
net.setBw("s121", "s131", 10)
net.addLink("s124", "s132")
net.setDelay("s124", "s132", 131)
net.setBw("s124", "s132", 10)
net.addLink("s124", "s125")
net.setDelay("s124", "s125", 118)
net.setBw("s124", "s125", 10)
net.addLink("s125", "s132")
net.setDelay("s125", "s132", 111)
net.setBw("s125", "s132", 10)
net.addLink("s125", "s142")
net.setDelay("s125", "s142", 128)
net.setBw("s125", "s142", 10)
net.addLink("s126", "s133")
net.setDelay("s126", "s133", 125)
net.setBw("s126", "s133", 10)
net.addLink("s126", "s132")
net.setDelay("s126", "s132", 110)
net.setBw("s126", "s132", 10)
net.addLink("s127", "s128")
net.setDelay("s127", "s128", 126)
net.setBw("s127", "s128", 10)
net.addLink("s131", "s132")
net.setDelay("s131", "s132", 123)
net.setBw("s131", "s132", 10)
net.addLink("s134", "s149")
net.setDelay("s134", "s149", 117)
net.setBw("s134", "s149", 10)
net.addLink("s134", "s142")
net.setDelay("s134", "s142", 125)
net.setBw("s134", "s142", 10)
net.addLink("s135", "s142")
net.setDelay("s135", "s142", 129)
net.setBw("s135", "s142", 10)
net.addLink("s136", "s137")
net.setDelay("s136", "s137", 127)
net.setBw("s136", "s137", 10)
net.addLink("s136", "s147")
net.setDelay("s136", "s147", 119)
net.setBw("s136", "s147", 10)
net.addLink("s137", "s148")
net.setDelay("s137", "s148", 114)
net.setBw("s137", "s148", 10)
net.addLink("s138", "s139")
net.setDelay("s138", "s139", 124)
net.setBw("s138", "s139", 10)
net.addLink("s139", "s141")
net.setDelay("s139", "s141", 111)
net.setBw("s139", "s141", 10)
net.addLink("s140", "s145")
net.setDelay("s140", "s145", 116)
net.setBw("s140", "s145", 10)
net.addLink("s141", "s145")
net.setDelay("s141", "s145", 127)
net.setBw("s141", "s145", 10)
net.addLink("s145", "s149")
net.setDelay("s145", "s149", 127)
net.setBw("s145", "s149", 10)
net.addLink("s146", "s147")
net.setDelay("s146", "s147", 121)
net.setBw("s146", "s147", 10)
net.addLink("s147", "s148")
net.setDelay("s147", "s148", 126)
net.setBw("s147", "s148", 10)
# Assignment strategy
net.mixed()
# Nodes general options
net.enableCpuPortAll()
#net.enablePcapDumpAll()
#net.enableLogAll()
net.enableCli()
net.startNetwork()
