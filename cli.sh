#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
DIR=$(cd "$(dirname "$0")"; pwd)
MDIR=$(dirname "$DIR")


PATH=$PATH:$DIR/bin
if [ -f bin/activate ];then
	source bin/activate
fi

export LC_ALL="en_US.UTF-8"

tgking_start_task()
{
    isStart=$(ps aux |grep 'task.py'|grep -v grep|awk '{print $2}')
    if [ "$isStart" == '' ];then
        echo -e "Starting mw-tasks... \c"
        cd $DIR && python3 task.py >> ${DIR}/logs/task.log 2>&1 &
        sleep 0.3
        isStart=$(ps aux |grep 'task.py'|grep -v grep|awk '{print $2}')
        if [ "$isStart" == '' ];then
            echo -e "\033[31mfailed\033[0m"
            echo '------------------------------------------------------'
            tail -n 20 $DIR/logs/task.log
            echo '------------------------------------------------------'
            echo -e "\033[31mError: mw-tasks service startup failed.\033[0m"
            return;
        fi
        echo -e "\033[32mdone\033[0m"
    else
        echo "Starting mw-tasks... mw-tasks (pid $(echo $isStart)) already running"
    fi
}

tgking_start(){
	gunicorn -c setting.py app:app
	#安全启动
	tgking_start_task
}


tgking_start_debug(){
	python3 task.py >> $DIR/logs/task.log 2>&1 &
	port=1314    
    if [ -f /opt/tg-king/data/port.pl ];then
        port=$(cat /opt/tg-king/data/port.pl)
    fi
    # gunicorn -b :${port} -k gevent -w 1 app:app
	gunicorn -b :${port} -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 app:app
}

tgking_start_debug2(){
	python3 task.py >> $DIR/logs/task.log 2>&1 &
	gunicorn -b :1314 -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1  app:app
}


tgking_stop()
{
	PLIST=`ps -ef|grep app:app |grep -v grep|awk '{print $2}'`
	for i in $PLIST
	do
	    kill -9 $i > /dev/null 2>&1
	done

	pids=`ps -ef|grep task.py | grep -v grep |awk '{print $2}'`
	arr=($pids)
    for p in ${arr[@]}
    do
    	kill -9 $p > /dev/null 2>&1
    done
}

case "$1" in
    'start') tgking_start;;
    'stop') tgking_stop;;
    'restart') 
		tgking_stop 
		tgking_start
		;;
	'debug') 
		tgking_stop 
		tgking_start_debug
		;;
	'debug2') 
		tgking_stop 
		tgking_start_debug2
		;;
esac