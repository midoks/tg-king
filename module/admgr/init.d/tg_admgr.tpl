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
    tg_start_cmd
    tg_start_task
}

tg_start_cmd(){ 
    isStart=`ps -ef|grep 'admgr_bot_cmd.py' |grep -v grep | awk '{print $2}'`
    if [ "$isStart" == '' ];then
        echo -e "starting admgr_bot_cmd... \c"
        cd $SP_PATH

        ids=`python3 {$SERVER_PATH}/tools.py tgbot_list admgr`
        ids=(${ids//,/ })
        
        for var in ${ids[@]}
        do
            python3 {$APP_PATH}/admgr_bot_cmd.py $var >> {$SERVER_PATH}/logs/module_admgr.log &
            echo "starting admgr_bot_cmd...${var}...done"
        done
        
    else
        echo "starting admgr_bot_cmd...(pid $(echo $isStart)) already running"
    fi
}


tg_start_task(){	

	isStart=`ps -ef|grep 'admgr_bot_task.py' |grep -v grep | awk '{print $2}'`
    if [ "$isStart" == '' ];then
        echo -e "starting admgr_bot_task... \c"
        cd $SP_PATH
        python3 {$APP_PATH}/admgr_bot_task.py >> {$SERVER_PATH}/logs/module_admgr.log &
        isStart=""
        while [[ "$isStart" == "" ]];
        do
            echo -e ".\c"
            sleep 0.5
            isStart=`ps -ef|grep 'admgr_bot_task.py' |grep -v grep | awk '{print $2}'`
            let n+=1
            if [ $n -gt 20 ];then
                break;
            fi
        done
        if [ "$isStart" == '' ];then
            echo -e "\033[31mfailed\033[0m"
            echo -e "\033[31mError: admgr_bot_task service startup failed.\033[0m"
            return;
        fi
        echo -e "\033[32mdone\033[0m"
    else
        echo "starting admgr_bot_task...(pid $(echo $isStart)) already running"
    fi
}


tg_stop(){
	echo -e "stopping admgr_bot_task ... \c";
    arr=`ps aux|grep 'admgr_bot_task.py'|grep -v grep|awk '{print $2}'`
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

