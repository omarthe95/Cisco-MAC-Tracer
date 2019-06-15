# Cisco MAC Tracer
Trace a host MAC address through Cisco access switches

* This Script works oly for **L2 Cisco Access Switches**
* First step the Script will ask if you want to **Collect MAC address table** from L2 Cisco Access Switches.
* If yes then a list of all interfacess that are not configured as Access port (such as Trunk, Port-channel, etc...) will be place for each device
* The Previous list will be used to extract MAC address table for Interfaces configured as **Access only**.
* Each MAC address table output will be save in a file with its device Hostname for searching process later.
* Then the Script will ask for a **Host (PC, Printer, or any end device) IP address**
* The IP address will be used in **Router ARP table** to get its MAC address.
* A Searching process will start with each ouput file to find the exact interface that match the **wanted MAC address **
* After that you will be asked if you want to access L2 Switch containing the extracted MAC address and **show run int (connected)**


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.



### Prerequisites:

* Linux OS (Recommended for Ubuntu 18.04)
* Python >=3.5 (pre-installed)
```
python3 --version
```

     
* SSH enabled and tested (connectivity)
```
ssh cisco@192.168.1.10
```

     
     
### Installing:

* Download the repository into a directory
```
git clone https://github.com/omarthe95/Cisco-MAC-Tracer.git
```

* Run setup.sh
```
bash setup.sh
```

* Edit L3 Cisco Routers (Gateway devices) **IPaddress_Routers.txt** file with your own management IP address, each device IP per line
```
nano IPaddress_Routers.txt
```

* Edit L2 Cisco Switches **IPaddress_Switches.txt** file with your own management IP address, each device IP per line
```
nano IPaddress_Switches.txt
```
* You may change the access credentials inside each python script individually, because the default access credentials into network devices is **cisco:Cisco123**




## Running the Scripts

We will start with each script with GIF to see it function



### Sequential.py

Entering each device **(one-by-one)** take so much time  

```
python3 Sequential.py
```
<img src="https://github.com/omarthe95/Resources/blob/master/Sequential.gif">

### MultiThreading.py

But executing it with *Threads* for each **independently** device of one another makes it faster

```
python3 MultiThreading.py
```
<img src="https://github.com/omarthe95/Resources/blob/master/MultiThreading.gif">

### Asyncio_Netdev.py

Concurrent the code with Asyncio that runs in a single thread will go beyond faster

```
python3 Asyncio_Netdev.py
```
<img src="https://github.com/omarthe95/Resources/blob/master/NetDev.gif">

## MultiThreading vs. Asynchronous
<img src="https://github.com/omarthe95/Resources/blob/master/vs1.png" width="500" height="312">





## Authors

* **Omar Adil** - *Network Engineer* - [Linkedin](https://www.linkedin.com/in/omar-adil-67218a134/)



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## Acknowledgments

Kirk Byers  
Python for Network Engineers  
https://pynet.twb-tech.com  

