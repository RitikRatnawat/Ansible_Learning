#!/bin/bash

sudo apt update && sudo apt upgrade -y
sudo apt-get update && sudo apt-get upgrade
sudo apt-add-repository ppa:ansible/ansible && sudo apt update
sudo apt install ansible -y && sudo apt install python3-pip -y
pip install boto3