#!/bin/bash

# get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# RSA key
RSA_ID="${DIR}/id_geni_ssh_rsa"

# node names
VM1="${1}@pcvm3-3.instageni.utc.edu"
VM2="${1}@pcvm3-4.instageni.utc.edu"
VM3="${1}@pcvm3-5.instageni.utc.edu"
VM4="${1}@pcvm3-6.instageni.utc.edu"
VM5="${1}@pcvm3-7.instageni.utc.edu"
VM6="${1}@pcvm3-8.instageni.utc.edu"
VM7="${1}@pcvm3-9.instageni.utc.edu"
VM8="${1}@pcvm3-10.instageni.utc.edu"

if [ "$2" == "seed" ]; then
    echo "GENERATING MOVIE DATA..."
    python generate_data.py
else
    rm server/movie_data.txt
fi

echo "UPLOADING SERVER FILES..."
for f in $( ls $DIR/server/ ); do
    sudo scp -r -i $RSA_ID $DIR/server/$f $VM1:~/
    sudo scp -r -i $RSA_ID $DIR/server/$f $VM2:~/
    sudo scp -r -i $RSA_ID $DIR/server/$f $VM3:~/
    sudo scp -r -i $RSA_ID $DIR/server/$f $VM4:~/
done

echo "UPLOADING CLIENT FILES..."
for f in $( ls $DIR/client/ ); do
    sudo scp -r -i $RSA_ID $DIR/client/$f $VM8:~/
done

echo "DONE"
