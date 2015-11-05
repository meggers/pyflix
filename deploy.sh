#!/bin/bash

# get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# RSA key
RSA_ID="${DIR}/id_geni_ssh_rsa"

# node names
VM1="mkellihe@pcvm3-3.instageni.utc.edu"
VM2="mkellihe@pcvm3-4.instageni.utc.edu"
VM3="mkellihe@pcvm3-5.instageni.utc.edu"
VM4="mkellihe@pcvm3-6.instageni.utc.edu"
VM5="mkellihe@pcvm3-7.instageni.utc.edu"
VM6="mkellihe@pcvm3-8.instageni.utc.edu"
VM7="mkellihe@pcvm3-9.instageni.utc.edu"
VM8="mkellihe@pcvm3-10.instageni.utc.edu"

echo "UPLOADING SERVER FILES..."

for f in $( ls $DIR/servers/ ); do
    sudo scp -r -i $RSA_ID $DIR/servers/$f $VM1:~/
    sudo scp -r -i $RSA_ID $DIR/servers/$f $VM2:~/
    sudo scp -r -i $RSA_ID $DIR/servers/$f $VM3:~/
    sudo scp -r -i $RSA_ID $DIR/servers/$f $VM4:~/
done

echo "UPLOADING CLIENT FILES..."

for f in $( ls $DIR/client/ ); do
    sudo scp -r -i $RSA_ID $DIR/client/$f $VM8:~/
done

echo "DONE"
