#!/bin/bash

workon koohnavard

git pull origin master

pip install -r requirements.txt
supervisorctl restart koohnavard

