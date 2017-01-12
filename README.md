###Cobbler PXE server with Ansible Vsphere deploy virtual machines

#####This article shows us how to configure Cobbler PXE sevrer for automatic deploying Virtual Machines in our Virtual Environment(vCphere). For that I wrote script. For this script I have used Python with libraries(Jinja2, Fabric, OS, Sys etc.) and Ansible with Vsphere module. Script gives us the following menu:
![run script](images/run.png)

#####Our topology will be as following:
![PXE topology](images/Topology.JPG)

#####Just try to execute script without CDROM inserted CentOS7 image:
![Without CDROM](images/without-cdrom.JPG)

#####Try to install with 1 Network card:
![Without one network card](images/1-net-card.JPG)

#####Try to normal installation process:
![normal installation](images/normal-result.JPG)

#####At the end just try from client machine to boot from network with VNC:
![F8 menu](images/F8.JPG)
![Enter](images/Enter.JPG)
![Choose-VNC](images/Choose-VNC.JPG)

#####Connecto with VNC viewer to this IP address:
![Connect to IP](images/VNC-IP.JPG)

#####At the end just connect to this IP with VNC viewer and use password which you typed in script execution time:
![VNC viewer](images/VNC-Vewer.JPG)
![Result of the work](images/Result-of-the-work.JPG)

#####To use this code use the following commands:
```sh
[root@ ~]# git clone https://github.com/jamalshahverdiev/c7pxeserver.git
[root@ ~]# cd c7pxeserver
[root@ ~]# ./install.py
```
