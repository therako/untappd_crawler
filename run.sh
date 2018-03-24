#!/bin/bash -e

username=$1
if [ -z $username ]; 
then
	echo "Please provide username with the script."
	exit 1
fi

pip install lxml requests

python untapped.py -u ${username} -o "${username}.json"
