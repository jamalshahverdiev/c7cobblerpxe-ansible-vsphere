###Cobbler PXE server with Ansible Vsphere deploy virtual machines

#####This article shows us how to configure Cobbler PXE sevrer for automatic deploying Virtual Machines in our Virtual Environment(vCphere). For that I wrote script. For this script I have used Python with libraries(Jinja2, Fabric, OS, Sys etc.) and Ansible with Vsphere module. Script gives us the following menu:
![run script](images/run.png)

#####If we choose 1 it will clone template machine for Cobbler PXE server(This will take some time). If we choose 2 it will install and configure PXE server. If we choose 3 it will deploy virtual machines with different setting which we configured before for each virtual machines. In my case I have used different static IP address. 

#####Our network Vmware topology will be as following:
![Vcenter topology](images/topology.png)

#####Let start from first point. Choose 1 look at Console and vSphere client:
![Option-1](images/option-1.png)
![Option-1-result1](images/option-1-result1.png)
![Option-1-result2](images/option-1-result2.png)

#####Get cloned virtual machine IP address. Login and password you must know because, you have created this. Don't forget insert CentOS7 image to virtual machine CDROM.
![PXEserverIP](images/pxecobblerIP.png)

#####Then press 2 and input details(Login, pass etc.) for already cloned new machine to install and configure Cobbler PXE server.
![Option-2](images/opntion-2.png)

#####At the end press 3 to deploy virtual machines with different setting in our ESXi's. We must input PXE credentials(IP, login, pass) and Vcenter credentials(IP, login, pass, Resource pool name, Datacenter name, Cluster name and ESXI IP).
![Option-3](images/option-3.png)
![Option-3-result1](images/option-3-result1.png)
![Option-3-result2](images/option3-result2.png)

#####And look at virtual machine console:
![Option-3-result3](images/option3-result3.png)

#####Result of our work must as following:
![End result](images/result-of-the-work.png)

#####I have used this scripts in my Fedora laptop. To use this script you must install Python and needed libraries. 
```sh
# dnf install python
# python -m ensurepip
$ sudo python -m pip install -r requirement.txt
```

#####To download this codes and run use the following commands:
```sh
$ git clone https://github.com/jamalshahverdiev/c7cobblerpxe-ansible-vpshere.git
$ cd c7cobblerpxe-ansible-vpshere
$ ./run.py
```
