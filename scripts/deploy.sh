#!/bin/bash

addr=$1
port=$2

echo Mocking deploy on $addr:$port
exit 0

ssh $addr -p $port "cd ~/koohnavard/ && bash ./scripts/self-deploy.sh"

