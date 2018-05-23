#!/bin/bash

sudo apt update
sudo apt install virtualenv -y
echo "creating virtual environment"
virtualenv venv -p python3
echo "activating virtual environment"
source venv/bin/activate
echo "installing deps"
pip install -r deploy/requirements.txt
echo "deactivating virtual environment"
deactivate
