#!/usr/bin/env sh

cd ../

DIRPATH=$(dirname $(pwd))
DIRNAME=$(basename $(pwd))

HOST=$1
KEY=$2
USER_LOGIN=$3
TARGETPATH=$4

alias ssh="ssh -i ~/.ssh/$KEY"

cd $DIRPATH; tar czf - $DIRNAME | ssh $USER_LOGIN@$HOST '(cd $TARGETPATH; \
    rm -rf *; tar xzf -)'
ssh $USER_LOGIN@$HOST "cd $TARGETPATH/$DIRNAME; make setup"
