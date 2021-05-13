#!/bin/bash

git config --global user.name "DiaboloKiat"
git config --global user.email "DiaboloKiat@gmail.com"

git status
echo "Enter your message"
read message
BRANCH=master


# push main
echo "------------------------------------------------------------------------"
echo "---------------------------push Seadrone--------------------------------"
echo "------------------------------------------------------------------------"
cd ~/Seadrone/
git add -A
git commit -m "${message}"
git push
