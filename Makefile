HOST ?= "" 
KEY ?= "~/.ssh"
USER_LOGIN ?= "root"
TARGETPATH ?= ""

.PHONY: setup deploy

setup:
	pip3 install --user -r requirements.txt
	mkdir -p logs
	touch logs/logs 
	touch logs/err 
	touch logs/out 
	chmod +x scripts/deploy.sh main.py

clean:
	rm out err logs/sys_logs.txt

restore_logs: clean_logs
	touch logs/sys_logs.txt err out 

deploy:
	echo "MAKE_HOST:${HOST}"
	sh -c scripts/deploy.sh ${HOST} ${KEY} ${USER_LOGIN} ${TARGETPATH}
