import pexpect, sys, threading, time, random
from subprocess import Popen, PIPE
import multiprocessing

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

topologies = ['Abilene', 'ChinaTelecom', 'IRISNetworks', 'BellSouth']
links = [] # network's links
expect_time = 1000000

# Change the number of try in the script
def update_try(n_try, topo_file):
    with open("controller.py","r") as script:
        lines = []
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
        links = []
        for line in f:
            if "net.addLink" in line:
                aux = line.rsplit('"')
                node1 = aux[1]
                node2 = aux[3]
                links.append([node1,node2])
    return links

# This will run the topology script
def run_shell_1(topo_file, lock, topo_links):
    lock.acquire()
    child = pexpect.spawn(f"sudo python {topo_file}.py")
    child.logfile = sys.stdout.buffer
    child.expect("mininet> ",timeout=expect_time)
    lock.release()

    time.sleep(1)

    lock.acquire()
    time.sleep(10)
    child.sendline("pingall")
    child.expect("mininet> ",timeout=expect_time)
    
    #Get random link that doesn't connect to a host
    index = random.randint(0,len(topo_links)-1)
    while 'h' in topo_links[index][0] or 'h' in topo_links[index][1]:
        index = random.randint(0,len(topo_links)-1)
    child.sendline(f"link {topo_links[index][0]} {topo_links[index][1]} down")
    child.expect("mininet> ")

    child.sendline("pingall")
    child.expect("mininet> ",timeout=expect_time)
    lock.release()

    time.sleep(1)

    lock.acquire()
    time.sleep(10)
    child.sendline("pingall")
    child.expect("mininet> ",timeout=expect_time)
    child.close()
    lock.release()

# This will run the script that sends the probes
def  run_shell_2(lock):
    # Must wait first for the other thread to do its tasks
    time.sleep(1)
    lock.acquire()
    time.sleep(5)
    child = pexpect.spawn(f"sudo python sendComputations.py")
    child.logfile = sys.stdout.buffer
    child.expect("Press your command...")
    child.sendline("x")
    child.expect("Press your command...")
    lock.release()

    time.sleep(3)

    lock.acquire()
    time.sleep(5)
    child.sendline("x")
    child.expect("Press your command...")
    time.sleep(5)
    child.sendline("x")
    child.expect("Press your command...")
    time.sleep(5)
    child.sendline("x")
    child.expect("Press your command...")
    child.close()
    lock.release()

def main():
    for topo in topologies:
        links = get_links(topo) # Update topology info
        for n in range(100):
            update_try(n+1, topo)
            
            print()
            print(f"{bcolors.WARNING}\nDEBUG: Try: {n+1} | Topo: {topo}\n{bcolors.ENDC}")

            # A lock for synchronization
            lock = multiprocessing.Lock()

            # Create 2 processes: One to run the topology and another to send probes
            shell_1 = multiprocessing.Process(target=run_shell_1, args=(topo, lock, links))
            shell_2 = multiprocessing.Process(target=run_shell_2, args=(lock,))

            shell_1.start()
            shell_2.start()

            shell_1.join()
            shell_2.join()          


if __name__ == "__main__":
    main()