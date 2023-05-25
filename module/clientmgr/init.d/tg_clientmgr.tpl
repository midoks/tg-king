#!/bin/sh
# chkconfig: 2345 55 25
# description: tg_admgr Service

### BEGIN INIT INFO
# Provides:          tg_admgr
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: starts tg_admgr
# Description:       starts the tg-king
### END INIT INFO

# Simple tg_admgr init.d script conceived to work on Linux systems
# as it does use of the /proc filesystem.

PATH=/usr/local/bin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export LANG=en_US.UTF-8


SP_PATH={$SERVER_PATH}
PATH=$PATH:$SP_PATH/bin

if [ -f $SP_PATH/bin/activate ];then
    source $SP_PATH/bin/activate
fi

tg_start(){
    tg_start_task
}

tg_start_task(){ 
    isStart=`ps -ef|grep 'clientmgr_client_task.py' |grep -v grep | awk '{print $2}'`
    if [ "$isStart" == '' ];then
        echo -e "starting clientmgr_client_task... \c"
        cd $SP_PATH

        ids=`python3 {$SERVER_PATH}/tools.py tgclient_list clientmgr`
        ids=(${ids//,/ })
        
        for var in ${ids[@]}
        do
            python3 {$APP_PATH}/clientmgr_client_task.py $var >> {$SERVER_PATH}/logs/module_clientmgr.log &
            echo "starting clientmgr_client_task...${var}...done"
        done
        
    else
        echo "starting clientmgr_client_task...(pid $(echo $isStart)) already running"
    fi
}



tg_stop(){
	echo -e "stopping clientmgr_client_task ... \c";
    arr=`ps aux|grep 'clientmgr_client_task.py'|grep -v grep|awk '{print $2}'`
    for p in ${arr[@]}
    do
        kill -9 $p > /dev/null 2>&1
    done
    echo -e "\033[32mdone\033[0m"
}

case "$1" in
    start)
		tg_start
        ;;
    stop)
        tg_stop
        ;;
	restart|reload)
		tg_stop
		sleep 0.3
		tg_start
		;;
    *)
        echo "Please use start or stop as first argument"
        ;;
esac

