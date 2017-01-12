#!/usr/bin/env bash

vms="web01 web02 db01 db02"

for vm in $vms
do
    echo yes | ezmomi destroy --name $vm
done
