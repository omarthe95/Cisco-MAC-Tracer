#!/usr/bin/python3

import netmiko, glob ,os ,sys, re, socket, json
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException


USER = 'cisco'
PASSWORD = 'Cisco123'

IPacc=""
cisco_ios_ACC = {'device_type': 'cisco_ios','ip': IPacc,'username': USER,'password': PASSWORD,'timeout':15}

#Read Routers IPs
Routers=[]
with open('IPaddress_Routers.txt') as f:
    for line in f:
        line = line.strip()
        try:
            socket.inet_aton(line)
            Routers.append(line)

        except socket.error:
            print ("Invalid IP address  " + line)
            sys.exit(1)

print ("This is Routers IPs: ")
print (str(Routers) + "\n")

# Input IP Address to Look for

IP = input ("Enter Host IP address :  ")
try:
    socket.inet_aton(IP)
except socket.error:
    print ("Invalid IP address \nexecpt ")
    sys.exit(1)

os.chdir("output/")

with open('dict.json') as json_file:  
    HOST_IP = json.load(json_file)


# Start Gathring ARP table info
for IPacc in Routers:
    cisco_ios_ACC = {'device_type': 'cisco_ios','ip': IPacc,'username': USER,'password': PASSWORD}
    try:
        ssh_session = ConnectHandler(**cisco_ios_ACC)
    except (AuthenticationException):
        print("Wrong Authentication >>> "+ (cisco_ios_ACC['ip']) + "\n")
        pass
    except (NetMikoTimeoutException):
        print("Timeout >>> "+ (cisco_ios_ACC['ip']) + "\n")
        pass
    except (EOFError):
        print("EOF Error >>> "+ (cisco_ios_ACC['ip']) + "\n")
        pass
    except (SSHException):
        print("Error SSH Exception >>> "+ (cisco_ios_ACC['ip']) + "\n")
        pass
    except Exception as unknown_error:
        print("Unkown Error >>> "+ (cisco_ios_ACC['ip']) + "\n")
        pass

    else:

        # Get the device Hostanme
        hostname = ssh_session.send_command('show run | inc host')
        hostname = hostname[9:]
        hostname.split(" ")
        
        # Extract MAC address from arp tabel
        output = ssh_session.send_command('show ip arp | inc ' + (IP))
        MAC = (re.findall(r'((?:[0-9a-f]{4}\.){2}[0-9a-f]{4})', output))
        MAC = ''.join(MAC) 
        if MAC == "":
           print ("MAC Not Found")
           sys.exit(1)
        else:
           print("Found MAC \n" )

   # Start Searching for the MAC in output files
        x=0
        for file in glob.glob('*'):
        
           with open(file) as f:
               contents = f.read()
               
           for line in contents.split("\n"):
               if MAC in line:
                   print ("#"*75)
                   print ("Found on >>>> " + file + "  <<<< ")
                   print (line)
                   print ("#"*75)
                   # Interface/port number
                   INT = line.rsplit(' ', 1)[1]

                   IntCheck = input ("\nDo you want to SSH into " + file + " with (show run int " + INT + ") ?\n (Yes or No) : ")
                   if IntCheck == "" or IntCheck == "Yes" or IntCheck == "yes" or IntCheck == "Y" or IntCheck == "y":
                       
                       cisco_ios_Router = {'device_type': 'cisco_ios','ip': HOST_IP[file],'username': USER,'password': PASSWORD}
                       ssh_session = ConnectHandler(**cisco_ios_Router)
                       output = ssh_session.send_command('show run int ' + (INT))
                       print (output)

                   elif IntCheck == "No" or IntCheck == "no" or IntCheck == "N" or IntCheck == "n":
                       print ("Tahnks Bye \n")
                       pass
                   else:
                       print("Invalid entry, Please enter yes or no.")
                       sys.exit(1)


                   x+=1
        if line is None: 
           print ("MAC Dont exist"+"\n")
        if x>1:
           print (">>>>>>> Duplication <<<<<<<<"+"\n")
        