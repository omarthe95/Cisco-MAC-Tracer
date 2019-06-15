#!/usr/bin/python3

import threading, os, time, sys ,socket, json
from multiprocessing import Queue
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException


HOST_IP={}
# Define username and password to login to all routers with
USER = 'cisco'
PASSWORD = 'Cisco123'

# Define Switches IPs
Switches=[]
with open('IPaddress_Switches.txt') as f:
    for line in f:
        line = line.strip()
        try:
            socket.inet_aton(line)
            Switches.append(line)

        except socket.error:
            print ("Invalid IP address  " + line)

print ("This is Switches IPs: \n")
print (Switches)


os.chdir("output/")


def ssh_session(switch, output_q):
    # Place what you want each thread to do here, for example connect to SSH, run a command, get output
    output_dict = {}
    # hostname = switch
    switch_d = {'device_type': 'cisco_ios', 'ip': switch, 'username': USER, 'password': PASSWORD,'timeout':15}

    # SSH Iteration
    try:
        ssh_session = ConnectHandler(**switch_d)
    except (AuthenticationException):
        print("Wrong Authentication >>> "+ (switch_d['ip']) + "\n")
        pass
    except (NetMikoTimeoutException):
        print("Timeout >>> "+ (switch_d['ip']) + "\n")
        pass
    except (EOFError):
        print("EOF Error >>> "+ (switch_d['ip']) + "\n")
        pass
    except (SSHException):
        print("Error SSH Exception >>> "+ (switch_d['ip']) + "\n")
        pass
    except Exception as unknown_error:
        print("Unkown Error >>> "+ (switch_d['ip']) + "\n")
        pass

    else:

        # Get the device Hostanme
        hostname = ssh_session.send_command('show run | inc host')
        hostname = hostname[9:]
        hostname.split(" ")
        # Make Dictionary 
        HOST_IP[hostname]=switch
    
        # Extract Trunk Interfaces
        Trunk_Int_List = []
        Trunk_output_1 = ssh_session.send_command("show int status | inc trunk")
        for line in Trunk_output_1.splitlines():
            line_1 = line[:9]
            line_1.strip()
            Trunk_Int_List.append(line_1)
        Trunk_Int_List_join = "|".join(Trunk_Int_List)
        Trunk_Int_List_join = Trunk_Int_List_join.replace(" ","")
        #print (Trunk_Int_List_join)

    
        # Put the Output into a List to use it later with threading
        output = ssh_session.send_command("show mac address | exclude All |" + Trunk_Int_List_join)
        output_dict[hostname] = output
        output_q.put(output_dict)
        f = open((hostname), "w")
        print((output), file=f)  # python 3.x

        f = open((hostname+"Trunk"), "w")
        print(("show mac address | exclude All |" + Trunk_Int_List_join), file=f)  # python 3.x



if __name__ == "__main__":

    output_q = Queue()

    # Start thread for each router in Switches list
    for switch in Switches:
        my_thread = threading.Thread(target=ssh_session, args=(switch, output_q))
        my_thread.start()

    my_thread.join()

# Save dic to file
json = json.dumps(HOST_IP)
f = open("dict.json","w+")
f.write(json)
f.close()
sys.exit(1)