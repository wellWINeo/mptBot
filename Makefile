HOST ?= "" 
KEY ?= "~/.ssh"
USER_LOGIN ?= "root"
TARGETPATH ?= ""

.PHONY: setup deploy

setup:
	pip3 install --user -r requirements.txt

deploy:
	DIR=${1:-`pwd`}
	DIRPATH=$(dirname $DIR)
	
	DIRNAME=$(basename $DIR)
	
	alias ssh='ssh -i ~/.ssh/'

	cd $DIRPATH; tar czf - $DIRNAME | ssh root@$HOST '(cd $TARGETPATH; rm -rf *; tar xzf -)' 

	ssh $USER_LOGIN@$HOST "cd $TARGETPATH/$DIRNAME; make setup"
