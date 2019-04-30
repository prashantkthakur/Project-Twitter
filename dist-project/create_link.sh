#!/usr/local/bin/bash
for i in $(cat ./workers);
do 
	echo "Creating link on $i"
	if [ ! -d "/s/$HOSTNAME/a/tmp/pthakur-kafka/" ];then
		mkdir -p /s/$HOSTNAME/a/tmp/pthakur-kafka/
	fi
	if [ ! -d "/tmp/pthakur-kafka" ];then 
		ssh $i 'cd /tmp; ln -s /s/$HOSTNAME/a/tmp/pthakur-kafka/ pthakur-kafka'; 
	else
		echo "Link already present!"
		ssh $i "ls -l /tmp/pthakur-kafka"
	fi
	if [ ! -d "/s/$HOSTNAME/a/tmp/pthakur-zookeeper" ];then
		mkdir -p /s/$HOSTNAME/a/tmp/pthakur-zookeeper
	fi
  if [ ! -d "/tmp/pthakur-zookeeper" ];then 
		ssh $i 'cd /tmp; ln -s /s/$HOSTNAME/a/tmp/pthakur-zookeeper/ pthakur-zookeeper; cd -'
  else
    echo "Link already present!"
    ssh $i "ls -l /tmp/pthakur-zookeeper"
  fi


done
