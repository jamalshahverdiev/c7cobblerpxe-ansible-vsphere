#!/usr/bin/env python2.7

import subprocess
import sys
from termcolor import colored, cprint

pxecobbler = colored('Cobbler', 'green', attrs=['bold', 'underline'])
template = colored('VM template', 'yellow', attrs=['bold', 'underline'])
virtms = colored('virtual machines', 'yellow', attrs=['bold', 'underline'])
exit = colored('exit', 'cyan', attrs=['bold', 'underline'])
enter = colored('Enter', 'cyan', attrs=['bold', 'underline'])
choose = ""

while choose != "3":
    print("Choose one of the following options:")
    print("""1. To create and deploy pxe server from '+template+' type 1 and press '+enter+'. 
   To create required VM template use link -> https://github.com/jamalshahverdiev/vagrant-vsphere-ansible""")
    print('2. To install and configure PXE server '+pxecobbler+', type 2 and press '+enter+'.')
    print('3. To deploy empty '+virtms+' type 3 and press '+enter+'. ')
    print('4. To '+exit+' press '+enter+'.')
    print('')
    choose = raw_input("  Please choose the installation option: ")
    print('')
    if choose == "1":
        subprocess.call("sudo ansible-playbook -i ansible-pxe-create/create_vm_hosts ansible-pxe-create/create_vms.yml", shell=True)
        print("")
        print("")
    elif choose == "2":
        print("")
        subprocess.call("c7pxecobbler-ansible-vpshere/install.py", shell=True)
        print("")
        print("")
    elif choose == "3":
        print("")
        subprocess.call("ansible-machines-create/install.py", shell=True)
        print("")
        sys.exit()
    elif choose == "":
        sys.exit()
    else:
        print("  You can choose options, only '1','2' or '3' !!!")
print("")
