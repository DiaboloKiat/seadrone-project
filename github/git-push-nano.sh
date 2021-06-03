#!/bin/bash

git config --global user.name "DiaboloKiat"
git config --global user.email "DiaboloKiat@gmail.com"

git status
git checkout devel-nano
echo "Enter your message"
read message
BRANCH=devel-nano


# push main
echo "------------------------------------------------------------------------"
echo "---------------------------push Seadrone--------------------------------"
echo "------------------------------------------------------------------------"
cd ~/seadrone-project/
git add -A
git commit -m "${message}"
git push origin devel-nano