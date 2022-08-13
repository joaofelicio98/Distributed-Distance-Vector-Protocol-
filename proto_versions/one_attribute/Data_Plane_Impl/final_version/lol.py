import pexpect, sys

child = pexpect.spawn(f"sudo mn")
child.logfile = sys.stdout.buffer
child.expect("mininet> ")
child.sendline("pingall")
child.expect("mininet> ")
child.sendline("link h1 s1 down")
child.expect("mininet> ")
child.sendline("pingall")
child.expect("mininet> ")
child.close()