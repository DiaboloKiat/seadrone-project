#!/bin/bash

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
