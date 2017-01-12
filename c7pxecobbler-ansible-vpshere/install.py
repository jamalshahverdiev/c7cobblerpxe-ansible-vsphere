#!/usr/bin/env python

import sys
import os
import jinja2
from termcolor import colored, cprint
from fabric.api import *
from fabric.tasks import execute
import getpass

#codepath = os.getcwd()
codepath = os.path.dirname(__file__)
jinjadir = codepath+'/jinja2temps/'
outputdir = codepath+'/output/'

templateLoader = jinja2.FileSystemLoader( searchpath=jinjadir )
templateEnv = jinja2.Environment( loader=templateLoader )

TEMPIFACE = 'ifcfg-name.j2'
TEMPPXEDEFTEMP = 'pxedefault.template.j2'
TEMPKICKS = 'CentOS-7.ks.j2'
TEMPCOBSETTINGS = 'cobbler_setting.j2'

tempiface = templateEnv.get_template( TEMPIFACE )
temppxedeft = templateEnv.get_template( TEMPPXEDEFTEMP )
tempks = templateEnv.get_template( TEMPKICKS )
tempcobsetgs = templateEnv.get_template( TEMPCOBSETTINGS )

pxeserver = colored('PXE server', 'green', attrs=['bold', 'underline'])
ipaddress = colored('IP address', 'green', attrs=['bold', 'underline'])
username = colored('username', 'green', attrs=['bold', 'underline'])
password = colored('password', 'magenta', attrs=['bold', 'underline'])
successfully = colored('successfully', 'green', attrs=['bold', 'underline'])
centos = colored('CentOS', 'yellow', attrs=['bold', 'underline'])
enter = colored('Enter', 'cyan', attrs=['bold', 'underline'])
root = colored('root', 'yellow', attrs=['bold', 'underline'])

print('Script install and configure Cobbler '+pxeserver+'.')
print('It needs '+ipaddress+', '+username+' and '+password+' to start process.')
env.host_string = raw_input('Please enter '+ipaddress+' of '+pxeserver+': ')
env.user = raw_input('Please enter '+username+' for UNIX/Linux server: ')
env.password = getpass.getpass('Please enter '+password+' for '+pxeserver+': ')

def tempconfiger(iface, uuidforiface, hwaddr, distro_name, rootps, lanip):
    tempVars = { "iface" : iface,
            "uuidforiface" : uuidforiface,
            "hwaddr": hwaddr,
            "distro_name": distro_name,
            "rootps": rootps,
            "lanip": lanip,
            }

    outputifaceText = tempiface.render( tempVars )
    outputpxeText = temppxedeft.render( tempVars )
    outputksText = tempks.render( tempVars )
    outputcobsetgsText = tempcobsetgs.render( tempVars )

    with open(outputdir+'ifcfg-'+iface+'', 'wb') as ifaceout:
        ifaceout.write(outputifaceText)

    with open(outputdir+'settings', 'wb') as cobsets:
        cobsets.write(outputcobsetgsText)

    with open(outputdir+'CentOS-7.ks', 'wb') as kickfile:
        kickfile.write(outputksText)

    with open(outputdir+'pxedefault.template', 'wb') as pxetemp:
        pxetemp.write(outputpxeText)

def variables():
    global osver
    osver = run('uname -s')
    global lintype
    lintype = run('cat /etc/centos-release | awk \'{ print $1 }\'')
    global getcosver
    getcosver = run('rpm -q --queryformat \'%{VERSION}\' centos-release')
    global netcards
    netcards = run('cat /proc/net/dev | egrep -v \'Inter|face|lo\' | cut -f1 -d\':\'')
    global checkcdrom
    checkcdrom = run('mount -o loop /dev/cdrom /mnt')
    global mountedcdrom
    mountedcdrom = run('cat /proc/mounts | grep iso9660 | head -1 | awk \'{ print $3 }\'')
    global netcardcount
    netcardcount = run('cat /proc/net/dev | egrep -v \'Inter|face|lo\' | cut -f1 -d\':\' | wc -l')
    global extcard
    extcard = run('ip a | grep '+env.host_string+' | awk \'{ print $NF }\'')

servicelist = ['cobblerd', 'dnsmasq', 'httpd', 'rsyncd', 'xinetd', 'network', 'firewalld', 'ntpd']

commands = ['yum update -y; yum -y install epel-release',
         'yum -y install net-tools bind-utils nload iftop wget git htop tcpdump ntpdate ntp telnet',
         'yum -y install cobbler cobbler-web dnsmasq syslinux pykickstart xinetd*',
         'ntpdate 0.asia.pool.ntp.org']

def prints():
    print('Please '+enter+' name of internal and external network card names!!!')
    print('Internal network card will be used to configure DHCP server!!!')
    print('External network card will be used to configure NAT for internal subnet 10.0.0.0/24!!!')
    print('')
    print('  Script connected to network card: '+extcard+'')
    print('')
    print(netcards)
    print('')

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

def put_func():
    put(jinjadir+'cobbler_dhcp.template', '/etc/cobbler/dhcp.template')
    put(jinjadir+'cobbler_dnsmasq.template', '/etc/cobbler/dnsmasq.template')
    put(jinjadir+'cobbler_modules.conf', '/etc/cobbler/modules.conf')
    put(jinjadir+'xinetd_tftp', '/etc/xinetd.d/tftp')
    put(outputdir+'ifcfg-'+intiface+'', '/etc/sysconfig/network-scripts/')
    put(outputdir+'CentOS-7.ks', '/var/lib/cobbler/kickstarts/CentOS-7.ks')
    put(outputdir+'pxedefault.template', '/etc/cobbler/pxe/pxedefault.template')
    put(outputdir+'settings', '/etc/cobbler/settings')

def after_install_vars():
    global cobblerservice
    cobblerservice = run('ps waux | grep \'/usr/bin/cobblerd\' | grep -v grep | awk \'{ print $12 }\'')
    global dmasqservice
    dmasqservice = run('ps waux| grep dnsmasq | grep -v grep | awk \'{ print $11 }\'')
    global httpdservice
    httpdservice = run('ps waux | grep \'httpd\' | grep \'^root\' | grep -v grep | awk \'{ print $11 }\'')
    global xinetdservice
    xinetdservice = run('ps waux | grep xinetd | grep -v grep | awk \'{ print $11 }\'')
    global netcardip
    netcardip = run('ifconfig '+intiface+' | grep \'inet \' | awk \'{ print $2 }\'')

def natconfiger(intiface, extiface):
    run('systemctl start firewalld')
    run('echo \'net.ipv4.ip_forward = 1\' >> /etc/sysctl.d/ip_forward.conf ; sysctl -w net.ipv4.ip_forward=1')
    run('echo NM_CONTROLLED=no >> /etc/sysconfig/network-scripts/ifcfg-'+extiface+'')
    run('echo ZONE=external >> /etc/sysconfig/network-scripts/ifcfg-'+extiface+'')
    run('firewall-cmd --permanent --zone=external --change-interface='+extiface+'')
    run('firewall-cmd --permanent --zone=internal --change-interface='+intiface+'')
    run('firewall-cmd --set-default-zone=external')
    run('firewall-cmd --complete-reload')
    run('firewall-cmd --zone=external --add-masquerade --permanent')
    run('firewall-cmd --permanent --direct --passthrough ipv4 -t nat -I POSTROUTING -o '+extiface+' -j MASQUERADE -s 10.0.0.0/24')
    run('firewall-cmd --permanent --zone=internal --add-service={dhcp,tftp,dns,http,https,nfs,ntp,ssh,ftp,vnc-server}')
    run('firewall-cmd --permanent --zone=internal --add-port={69/udp,4011/udp}')
    run('firewall-cmd --complete-reload')

def importos(distro_name, intiface):
    run('mount -o loop /dev/cdrom /mnt/')
    run('cobbler import --arch=x86_64 --path=/mnt --name=CentOS-7')
    run('umount /mnt')
    run('cobbler profile edit --name='+distro_name+' --kickstart=/var/lib/cobbler/kickstarts/CentOS-7.ks')
    run('cobbler system add --name=COS7 --profile='+distro_name+'  --interface='+intiface+' --netboot-enabled=1 --static=1')
    run('cobbler sync')

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

        if checkcdrom == '':
            pass
        elif mountedcdrom == 'iso9660':
            print('CDROM is already mounted!!!')
            sys.exit()
        else:
            print('Please insert CentOS7 image to your server CDROM and try again!!!')
            sys.exit()

        if netcardcount < '2':
            print('Your server network card must be minimum 2. Please add second network card and try again!!!')
            sys.exit()
        else:
            pass

        print('  Please be patient script will install and configure all needed packages!!!')
        print('')

        run('systemctl stop NetworkManager; systemctl disable NetworkManager')

	for comm in commands:
            run(comm)

        prints()
        extiface = raw_input('Please '+enter+' external network card name for NAT configuration: ')
        intiface = raw_input('Please '+enter+' internal network card name for DHCP sevrer: ')
        hwaddr = run('ifconfig '+intiface+'| grep ether | awk \'{ print $2 }\'')
        uuidforiface = run('uuidgen '+intiface+'')
        distro_name = 'CentOS-7-x86_64'
        root_pass()
        lanip = '10.0.0.1'
        rootps = run('echo '+rootpass+' | openssl passwd -1 -stdin')
        print('Please be patient script create template files and copy the content of the CDROM to the file system!!!')
        tempconfiger(intiface, uuidforiface, hwaddr, distro_name, rootps, lanip)
        natconfiger(intiface, extiface)
        put_func()

        for service in servicelist:
            run('systemctl restart '+service+'; systemctl enable '+service+'')

        run('cobbler get-loaders ; cobbler sync')

        importos(distro_name, intiface)

        after_install_vars()

        if cobblerservice == '/usr/bin/cobblerd' and dmasqservice == '/usr/sbin/dnsmasq' and httpdservice == '/usr/sbin/httpd' and xinetdservice == '/usr/sbin/xinetd' and netcardip == '10.0.0.1':
            print('')
            print('All services '+successfully+' installed and configured!')
            sys.exit()
        else:
            print('')
            print('There is some problem with installation. One of the services (dnsmasq, vsftpd) or '+intiface+' '+ipaddress+' is not configured properly!!!')
            print('Please check SeLinux, firewalld!!!')
            sys.exit()
