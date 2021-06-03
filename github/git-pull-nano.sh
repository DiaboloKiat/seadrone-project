#! /bin/bash

# echo "password: $2"
git checkout devel-nano
BRANCH=devel-nano
if [ ! -z "$1" ]; then
    echo "pull branch: $1"
    BRANCH=$1
fi

echo "------------------------------------------------------------------------"
echo "---------------------------pull Seadrone--------------------------------"
echo "------------------------------------------------------------------------"
git pull

CONFLICTS=$(git ls-files -u | wc -l)
if [ "$CONFLICTS" -gt 0 ] ; then
   echo "There is conflict in subt-system. Aborting"
   return 1
fi

cd ~/seadrone-project
return 0