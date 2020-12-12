#!/usr/bin/env sh

DIRPATH=$(dirname $(pwd))
DIRNAME=$(basename $(pwd))

set HOST=$1
set KEY=$2
set USER_LOGIN=$3
set TARGETPATH=$4

alias ssh="ssh -i ~/.ssh/$KEY"
echo "ssh -i ~/.ssh/$KEY"

cd $DIRPATH; tar czf - $DIRNAME | ssh $USER_LOGIN@$HOST '(cd '$TARGETPATH'&& \
    rm -rf * && tar xzf -)'
ssh $USER_LOGIN@$HOST "cd $TARGETPATH/$DIRNAME; make setup"
