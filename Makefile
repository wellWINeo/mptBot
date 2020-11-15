HOST ?= "" 
KEY ?= "~/.ssh"
USER_LOGIN ?= "root"
TARGETPATH ?= ""
#DIRPATH=$(dirname $(pwd))
#DIRNAME=$(basename $(pwd))

.PHONY: setup deploy

setup:
	pip3 install --user -r requirements.txt
	touch {log/sys_logs.txt, err, out}
	chmod +x {setup/scripts, main.py}

deploy:
	sh -c scripts/deploy.sh ${HOST} ${KEY} ${USER_LOGIN} ${TARGETPATH}
