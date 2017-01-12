#!/usr/bin/env bash

OSBSD=`uname -s` 
FVER=`uname -r | cut -f1 -d'.'`

if [ "$OSBSD" == "FreeBSD" ] && [ "$FVER" = "10" ]
then
    if [ -f /usr/local/bin/python3.4 ] && [ -f /usr/local/bin/python2.7 ]
    then
        echo "This is FreeBSD server!!!"
        echo "You have installed Python2.7 and Python3.4"
        exit 0
    else
        echo "This is FreeBSD server!!!" 
        /usr/sbin/pkg install -y bash vim bash-completion
        /usr/sbin/pkg install -y python27 python34
        /usr/local/bin/python3.4 -m ensurepip
        /usr/local/bin/python3.4 -m pip install --upgrade pip
        /usr/local/bin/python3.4 -m pip install fabric
        /usr/local/bin/python3.4 -m pip install netmiko
        /usr/local/bin/python3.4 -m pip install pexpect
        /usr/local/bin/python3.4 -m pip install Jinja2
        /usr/local/bin/python3.4 -m pip install termcolor
        /usr/local/bin/python2.7 -m ensurepip
        /usr/local/bin/python2.7 -m pip install --upgrade pip
        /usr/local/bin/python2.7 -m pip install fabric
        /usr/local/bin/python2.7 -m pip install netmiko
        /usr/local/bin/python2.7 -m pip install pexpect
        /usr/local/bin/python2.7 -m pip install Jinja2
        /usr/local/bin/python2.7 -m pip install termcolor
        echo "******************************************************"
        echo "Python2.7 and Python3.4 is installed with libraries!!!"
        echo "******************************************************"
    fi
else
    echo -e "\n"
fi

if [ -f /etc/issue ] && [ -f /etc/redhat-release ]
then
    if [ -f /usr/local/bin/python3.4 ] && [ -f /usr/local/bin/python2.7 ]
    then
        echo "This is CentOS server!!!"
        echo "You have installed Python2.7 and Python3.4"
        exit 0
    else
        echo "This is CentOS server!!!"
        yum -y groupinstall "Development tools"
        yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel gcc wget
        yum -y install epel-release
        cd /usr/src
        wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
        tar xzf Python-2.7.10.tgz
        cd Python-2.7.10
        ./configure
        make && make altinstall
        echo "*************************************"
        echo "Python2.7 already installed"
        echo "*************************************"
        cd /usr/src
        wget https://www.python.org/ftp/python/3.4.4/Python-3.4.4rc1.tgz
        tar xzf Python-3.4.4rc1.tgz
        cd Python-3.4.4rc1
        ./configure
        make && make altinstall
        /usr/local/bin/python3.4 -m ensurepip
        /usr/local/bin/python3.4 -m pip install --upgrade pip
        /usr/local/bin/python3.4 -m pip install fabric
        /usr/local/bin/python3.4 -m pip install netmiko
        /usr/local/bin/python3.4 -m pip install pexpect
        /usr/local/bin/python3.4 -m pip install Jinja2
        /usr/local/bin/python3.4 -m pip install termcolor
        /usr/local/bin/python2.7 -m ensurepip
        /usr/local/bin/python2.7 -m pip install --upgrade pip
        /usr/local/bin/python2.7 -m pip install fabric
        /usr/local/bin/python2.7 -m pip install netmiko
        /usr/local/bin/python2.7 -m pip install pexpect
        /usr/local/bin/python2.7 -m pip install Jinja2
        /usr/local/bin/python2.7 -m pip install termcolor
        echo "******************************************************"
        echo "Python2.7 and Python3.4 is installed with libraries!!!"
        echo "******************************************************"
    fi
else
    echo -e "\n"
fi
