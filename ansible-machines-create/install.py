#!/usr/bin/env python

import sys
import os
import jinja2
from termcolor import colored, cprint
from fabric.api import *
from fabric.tasks import execute
import getpass
import subprocess
import time 

codepath = os.path.dirname(__file__)
#codepath = os.getcwd()
jinjadir = codepath+'/jinja2temps/'
outputdir = codepath+'/output/'

templateLoader = jinja2.FileSystemLoader( searchpath=jinjadir )
templateEnv = jinja2.Environment( loader=templateLoader )

TEMPKICKS = 'CentOS-7.ks.j2'
TEMPYML = 'vms.yml.j2'
TEMPINVENT = 'vm_hosts.j2'

tempks = templateEnv.get_template( TEMPKICKS )
tempyml = templateEnv.get_template( TEMPYML )
tempinvt = templateEnv.get_template( TEMPINVENT )

pxeserver = colored('PXE server', 'green', attrs=['bold', 'underline'])
vcserver = colored('Vcenter server', 'blue', attrs=['bold', 'underline'])
ipaddress = colored('IP address', 'green', attrs=['bold', 'underline'])
username = colored('username', 'green', attrs=['bold', 'underline'])
password = colored('password', 'magenta', attrs=['bold', 'underline'])
centos = colored('CentOS', 'yellow', attrs=['bold', 'underline'])
enter = colored('Enter', 'cyan', attrs=['bold', 'underline'])
root = colored('root', 'yellow', attrs=['bold', 'underline'])

print('Script deploy virtual machines in Vcenter.')
print('It needs '+ipaddress+', '+username+' and '+password+' to start process.')
env.host_string = raw_input('Please enter '+ipaddress+' of '+pxeserver+': ')
env.user = raw_input('Please enter '+username+' for '+pxeserver+': ')
env.password = getpass.getpass('Please enter '+password+' for '+pxeserver+': ')

vcenterip = raw_input(' '+enter+' '+ipaddress+' of the '+vcserver+': ')
vcenterusername = raw_input(' '+enter+' the '+username+' of the '+vcserver+': ')
vcenterpassword = getpass.getpass(' '+enter+' the '+password+' of the '+vcserver+': ')
resourcepoolname = raw_input(' '+enter+' the Resource pool name of the '+vcserver+': ')
datacentername = raw_input(' '+enter+' the Datacenter name of the '+vcserver+': ')
esxihostip = raw_input(' '+enter+' the ESXI '+ipaddress+': ')
clustername = raw_input(' '+enter+' the Cluster name of the '+vcserver+': ')

def root_pass():
    print('')
    print('Please remember entered '+root+' user '+password+'. It will be set '+password+' of user '+root+' for OS installation over kickstart.')
    print('')
    global rootpass
    rootpass = getpass.getpass('  Please '+enter+' '+root+' user '+password+': ')
    global rootpass1
    rootpass1 = getpass.getpass('  Please repeat '+password+' of the '+root+' user: ')
    print('')

    while rootpass != rootpass1:
        print('')
        print(' Entered passwords must be the same. Please '+enter+' passwords again. ')
        rootpass = getpass.getpass('  Please '+enter+' '+root+' user '+password+': ')
        rootpass1 = getpass.getpass('  Please repeat '+password+' of the '+root+' user: ')

        if rootpass == rootpass1:
            print('')
            print(' The '+password+' set successfully!')
            break
        print(' Entered passwords must be the same. Please '+enter+' passwords again. ')

root_pass()

gateip = '10.0.0.1'
submask = '255.255.255.0'
distro_name = 'CentOS-7-x86_64'

def tempconfiger(ifip, submask, distro_name, rootps, gateip, vcenterip, vcenterusername, vcenterpassword, resourcepoolname, datacentername, esxihostip, clustername, vm_name):
    tempVars = { "ifip" : ifip,
            "submask" : submask,
            "gateip": gateip,
            "distro_name": distro_name,
            "rootps": rootps,
            "lanip": gateip,
            "vcenterip": vcenterip,
            "vcenterusername": vcenterusername,
            "vcenterpassword": vcenterpassword,
            "resourcepoolname": resourcepoolname,
            "datacentername": datacentername,
            "esxihostip": esxihostip,
            "clustername": clustername,
            "vm_name": vm_name,
            }

    outputksText = tempks.render( tempVars )
    outputymlText = tempyml.render( tempVars )
    outputinvtText = tempinvt.render( tempVars )

    with open(outputdir+'CentOS-7.ks', 'wb') as kickfile:
        kickfile.write(outputksText)

    with open(outputdir+'vms.yml', 'wb') as ymlfile:
        ymlfile.write(outputymlText)

    with open(outputdir+'vm_hosts', 'wb') as hostsfile:
        hostsfile.write(outputinvtText)

def variables():
    global osver
    osver = run('uname -s')
    global lintype
    lintype = run('cat /etc/centos-release | awk \'{ print $1 }\'')
    global getcosver
    getcosver = run('rpm -q --queryformat \'%{VERSION}\' centos-release')

virtmaes = ['web01', 'web02', 'db01', 'db02']

def put_func():
    put(outputdir+'CentOS-7.ks', '/var/lib/cobbler/kickstarts/CentOS-7.ks')
    run('cobbler sync')

def executer():
    tempconfiger(ifip, submask, distro_name, rootps, gateip, vcenterip, vcenterusername, vcenterpassword, resourcepoolname, datacentername, esxihostip, clustername, vm_name)
    put_func()
    subprocess.call('sudo ansible-playbook -i '+outputdir+'/vm_hosts '+outputdir+'/vms.yml', shell=True)
    time.sleep(100)

with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
    variables()

    if osver == 'Linux' and lintype == 'CentOS':
        print('')
        print('OS type Linux '+centos+'.')

        if getcosver == '6':
            print('Version is "6"!')
        elif getcosver == '7':
            print('Version is "7"!')
            print('')

        rootps = run('echo '+rootpass+' | openssl passwd -1 -stdin')

        for i in range(2, 6):
            ifip = '10.0.0.%s' % i

            for vm_name in virtmaes:
                if ifip == '10.0.0.2' and vm_name == 'web01':
                    executer()
                elif ifip == '10.0.0.3' and vm_name == 'web02':
                    executer()
                elif ifip == '10.0.0.4' and vm_name == 'db01':
                    executer()
                elif ifip == '10.0.0.5' and vm_name == 'db02':
                    executer()
