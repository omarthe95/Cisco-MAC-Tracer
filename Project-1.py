#!/usr/bin/python3

import time,os,sys

start = time.time()

os.chdir("/home/bin/P1/Script/")

IntCheck = input ("\nDo you want to Collect MAC address from CISCO Access Switches ?\n (Yes or No) : ")
if IntCheck == "" or IntCheck == "Yes" or IntCheck == "yes" or IntCheck == "Y" or IntCheck == "y":
    print ("<<<<<<<<<<<<  Start Collecting  >>>>>>>>>>> \n")                   
    os.system("python3 MAC_Table_Cisco_Access_Layer_Threaded.py")

    print ("<<<<<<<<<<<<  Start Searching  >>>>>>>>>>> \n")
    os.system("python3 Search_By_Router_ARP.py")

elif IntCheck == "No" or IntCheck == "no" or IntCheck == "N" or IntCheck == "n":
    print ("<<<<<<<<<<<<  Start Searching  >>>>>>>>>>> \n")
    os.system("python3 Search_By_Router_ARP.py")
    pass

else:
    print("Invalid entry, Please enter yes or no.")
    sys.exit(1)



end = time.time()
total = int(end - start)
print("\n Elapsd Time: " + str(total) + " Sec\n")
