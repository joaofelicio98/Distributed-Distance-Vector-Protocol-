import pexpect, sys, threading, time, random
from subprocess import Popen, PIPE

topologies = ['Abilene', 'China Telecom', 'IRIS Networks', 'Bell South']
lines = []
n_try = 1
log_file = "test_logs.txt" # File where we write the logs
links = [] # network's links

# Change the number of try in the script
def update_try(topo_file):
    with open("controller.py","r") as script:
        for line in script:
            if "# Number of try" in line:
                line = f"        self.Try = {n_try} # Number of try\n"
            elif "# Topology I am currently using" in line:
                line = f'        self.topology = "{topo_file}" # Topology I am currently using\n'
            lines.append(line)

    with open("controller_tmp.py","w") as f:
        for line in lines:
            f.write(line)
    
    # Replace the controller.py with the temporary file
    p = Popen('mv controller_tmp.py controller.py', shell=True,
            stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()

# Save all links in a list
def get_links(topo_file):
    with open(topo_file+".py","r") as f:
        for line in f:
            if "net.addLink" in line:
                aux = line.rsplit('"')
                node1 = aux[1]
                node2 = aux[3]
                links.append([node1,node2])

# This will run the topology script
def run_shell_1(topo_file, lock):
    lock.acquire()
    print()
    print("ENTERED SHELL 1")
    print()
    # Logs to write on the log_file
    logs=[]

    child = pexpect.spawn(f"sudo python {topo_file}.py")
    #child.logfile = sys.stdout.buffer
    child.expect("mininet> ")
    logs.append(child.before.decode('utf-8').splitlines())
    lock.release()
    print()
    print("SHELL 1 FIRST RELEASE")
    print()

    lock.acquire()
    print()
    print("SHELL 1 AQUIRED")
    print()
    index = random.randint(0,len(links))
    print()
    print(f"NODE1 = {links[index][0]} | NODE2 = {links[index][1]}")
    print()
    child.sendline(f"link {links[index][0]} {links[index][1]} down")
    child.expect("mininet> ")
    logs.append(child.before.decode('utf-8').splitlines())

    child.sendline("pingall")
    child.expect("mininet> ",timeout=1000)
    print("X" in child.before)
    print()
    print(child.before)
    logs.append(child.before.decode('utf-8').splitlines())
    lock.release()

    lock.acquire()
    print()
    print("Will start to print logs!")
    print()
    child.sendline("pingall",timeout = 400)
    child.expect("mininet> ")
    print( )
    print(child.before)
    print()
    logs.append(child.before.decode('utf-8').splitlines())
    child.close()

    # Print logs to the file
    with open(log_file,"a") as f:
        for l in logs:
            for line in l:
                f.write(line + "\n")

    lock.release()

    

#    logs = []
#    child = pexpect.spawn(f"sudo python {topo_file}.py")
#    child.logfile = sys.stdout.buffer
#    child.expect("mininet> ")
#    logs.append(child.before.decode('utf-8').splitlines())
#    child.sendline("pingall")
#    child.expect("mininet> ")
#    logs.append(child.before.decode('utf-8').splitlines())
#    for x in range(len(topologies)):
#        if topo_file == topologies[x]
#        break
#    index = random.randint(0,len(topologies[x]))
#    child.sendline(f"link {topologies[x][index][0]} {topologies[x][index][0]} down")
#    #TODO Give the lock to wait for further instructions
#    child.close()

    #with open(log_file,"w") as f:

# This will run the script that sends the probes
def  run_shell_2(lock):
    # Must wait first for the other thread to do its tasks 
    while lock.locked() == False:
        print()
        print("GOT INTO THE WHILE")
        print()
        continue
    print()
    print("GOT OUT OF THE WHILE")
    print()
    lock.acquire()
    print()
    print("ACQUIRED!!")
    print()
    child = pexpect.spawn(f"sudo python sendComputations.py")
    child.expect("Press your command...")
    child.sendline("x")
    child.expect("Press your command...")
    lock.release()

    lock.acquire()
    print()
    print("Will start to recover the failed link!")
    print()    
    child.sendline("x")
    child.expect("Press your command...")
    child.sendline("x")
    child.expect("Press your command...")
    child.sendline("x")
    child.expect("Press your command...")
    child.close()
    lock.release()

def main():
    #TODO make a loop to go through each topo 

    # A lock for synchronization
    lock = threading.Lock()
    # Create 2 threads: One to run the topology and another to send probes
    shell_1 = threading.Thread(target=run_shell_1, args=(topologies[0], lock))
    shell_2 = threading.Thread(target=run_shell_2, args=(lock,))

    update_try(topologies[0])
    get_links(topologies[0])

    shell_1.start()
    shell_2.start()

    shell_1.join()
    shell_2.join()
    failed_links=[]


if __name__ == "__main__":
    main()