#!/bin/bash
# chkconfig: 2345 55 25
# description: TGKING Cloud Service

### BEGIN INIT INFO
# Provides:          Midoks
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: starts TGKING
# Description:       starts the TGKING
### END INIT INFO


PATH=/usr/local/bin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export LANG=en_US.UTF-8

TGKING_PATH={$SERVER_PATH}
PATH=$PATH:$TGKING_PATH/bin


if [ -f $TGKING_PATH/bin/activate ];then
    source $TGKING_PATH/bin/activate
fi

tgking_start_panel()
{
    isStart=`ps -ef|grep 'gunicorn -c setting.py apptg:app' |grep -v grep|awk '{print $2}'`
    if [ "$isStart" == '' ];then
        echo -e "starting TGKING-Panel... \c"
        cd $TGKING_PATH &&  gunicorn -c setting.py apptg:app
        port=$(cat ${TGKING_PATH}/data/port.pl)
        isStart=""
        while [[ "$isStart" == "" ]];
        do
            echo -e ".\c"
            sleep 0.5
            isStart=$(lsof -n -P -i:$port|grep LISTEN|grep -v grep|awk '{print $2}'|xargs)
            let n+=1
            if [ $n -gt 20 ];then
                break;
            fi
        done
        if [ "$isStart" == '' ];then
            echo -e "\033[31mfailed\033[0m"
            echo '------------------------------------------------------'
            tail -n 20 ${TGKING_PATH}/logs/error.log
            echo '------------------------------------------------------'
            echo -e "\033[31mError: TGKING-Panel service startup failed.\033[0m"
            return;
        fi
        echo -e "\033[32mdone\033[0m"
    else
        echo "starting TGKING-Panel... TGKING(pid $(echo $isStart)) already running"
    fi
}


tgking_start_task()
{
    isStart=$(ps aux |grep 'tgking-task.py'|grep -v grep|awk '{print $2}')
    if [ "$isStart" == '' ];then
        echo -e "Starting TGKING-Task... \c"
        cd $TGKING_PATH && python3 tgking-task.py >> ${TGKING_PATH}/logs/task.log 2>&1 &
        sleep 0.3
        isStart=$(ps aux |grep 'tgking-task.py'|grep -v grep|awk '{print $2}')
        if [ "$isStart" == '' ];then
            echo -e "\033[31mfailed\033[0m"
            echo '------------------------------------------------------'
            tail -n 20 $TGKING_PATH/logs/task.log
            echo '------------------------------------------------------'
            echo -e "\033[31mError: TGKING-Panel service startup failed.\033[0m"
            return;
        fi
        echo -e "\033[32mdone\033[0m"
    else
        echo "starting TGKING-Panel... TASK (pid $(echo $isStart)) already running"
    fi
}

tgking_start()
{
    tgking_start_task
	tgking_start_panel
}

tgking_stop_task()
{
    if [ -f $TGKING_PATH/tmp/panelTask.pl ];then
        echo -e "\033[32mthe task is running and cannot be stopped\033[0m"
        exit 0
    fi

    echo -e "Stopping TGKING-Panel... \c";
    pids=$(ps aux | grep 'tgking-task.py'|grep -v grep|awk '{print $2}')
    arr=($pids)
    for p in ${arr[@]}
    do
        kill -9 $p  > /dev/null 2>&1
    done
    echo -e "\033[32mdone\033[0m"
}

tgking_stop_panel()
{
    echo -e "Stopping TGKING-Panel... \c";
    arr=`ps aux|grep 'gunicorn -c setting.py apptg:app'|grep -v grep|awk '{print $2}'`
    for p in ${arr[@]}
    do
        kill -9 $p > /dev/null 2>&1
    done
    
    pidfile=${mw_path}/logs/tgking.pid
    if [ -f $pidfile ];then
        rm -f $pidfile
    fi
    echo -e "\033[32mdone\033[0m"
}

tgking_stop()
{
    tgking_stop_task
    tgking_stop_panel
}

tgking_status()
{
    isStart=$(ps aux|grep 'gunicorn -c setting.py app:app'|grep -v grep|awk '{print $2}')
    if [ "$isStart" != '' ];then
        echo -e "\033[32mTGKING-Panel (pid $(echo $isStart)) already running\033[0m"
    else
        echo -e "\033[31mTGKING-Panel not running\033[0m"
    fi
    
    isStart=$(ps aux |grep 'tgking-task.py'|grep -v grep|awk '{print $2}')
    if [ "$isStart" != '' ];then
        echo -e "\033[32mTGKING-TASK (pid $isStart) already running\033[0m"
    else
        echo -e "\033[31mTGKING-TASK not running\033[0m"
    fi
}


tgking_reload()
{
	isStart=$(ps aux|grep 'gunicorn -c setting.py apptg:app'|grep -v grep|awk '{print $2}')
    
    if [ "$isStart" != '' ];then
    	echo -e "reload TGKING-Panel... \c";
	    arr=`ps aux|grep 'gunicorn -c setting.py apptg:app'|grep -v grep|awk '{print $2}'`
		for p in ${arr[@]}
        do
                kill -9 $p
        done
        cd $TGKING_PATH && gunicorn -c setting.py apptg:app
        isStart=`ps aux|grep 'gunicorn -c setting.py apptg:app'|grep -v grep|awk '{print $2}'`
        if [ "$isStart" == '' ];then
            echo -e "\033[31mfailed\033[0m"
            echo '------------------------------------------------------'
            tail -n 20 $TGKING_PATH/logs/error.log
            echo '------------------------------------------------------'
            echo -e "\033[31mError: TGKING-Panel service startup failed.\033[0m"
            return;
        fi
        echo -e "\033[32mdone\033[0m"
    else
        echo -e "\033[31mTGKING-Panel not running\033[0m"
        mw_start
    fi
}

tgking_close(){
    echo 'True' > $TGKING_PATH/data/close.pl
}

tgking_open()
{
    if [ -f $TGKING_PATH/data/close.pl ];then
        rm -rf $TGKING_PATH/data/close.pl
    fi
}

error_logs()
{
	tail -n 100 $TGKING_PATH/logs/error.log
}

tgking_update()
{
    curl --insecure -fsSL  https://raw.githubusercontent.com/midoks/tg-king/main/scripts/update.sh | bash
}

tgking_update_dev()
{
    curl --insecure -fsSL  https://raw.githubusercontent.com/midoks/tg-king/dev/scripts/update_dev.sh | bash
    cd /opt/tg-king
}


tgking_close_admin_path(){
    if [ -f $TGKING_PATH/data/admin_path.pl ]; then
        rm -rf $TGKING_PATH/data/admin_path.pl
    fi
}

tgking_force_kill()
{
    PLIST=`ps -ef|grep apptg:app |grep -v grep|awk '{print $2}'`
    for i in $PLIST
    do
        kill -9 $i
    done

    pids=`ps -ef|grep tgking-task.py | grep -v grep |awk '{print $2}'`
    arr=($pids)
    for p in ${arr[@]}
    do
        kill -9 $p
    done
}

tgking_debug(){
    tgking_stop
    tgking_force_kill

    port=1314    
    if [ -f $TGKING_PATH/data/port.pl ];then
        port=$(cat $TGKING_PATH/data/port.pl)
    fi

    if [ -d /opt/tg-king ];then
        cd /opt/tg-king
    fi
    gunicorn -b :$port -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1  app:app
}

case "$1" in
    'start') tgking_start;;
    'stop') tgking_stop;;
    'reload') tgking_reload;;
    'restart') 
        tgking_stop
        tgking_start;;
    'restart_panel')
        tgking_stop_panel
        tgking_start_panel;;
    'restart_task')
        tgking_stop_task
        tgking_start_task;;
    'status') tgking_status;;
    'logs') error_logs;;
    'close') tgking_close;;
    'open') tgking_open;;
    'update') mw_update;;
    'update_dev') mw_update_dev;;
    'close_admin_path') tgking_close_admin_path;;
    'debug') tgking_debug;;
    'default')
        cd $TGKING_PATH
        port=1314
        
        if [ -f $TGKING_PATH/data/port.pl ];then
            port=$(cat $TGKING_PATH/data/port.pl)
        fi

        if [ ! -f $TGKING_PATH/data/default.pl ];then
            echo -e "\033[33mInstall Failed\033[0m"
            exit 1
        fi

        password=$(cat $TGKING_PATH/data/default.pl)
        if [ -f $TGKING_PATH/data/domain.conf ];then
            address=$(cat $TGKING_PATH/data/domain.conf)
        fi
        if [ -f $TGKING_PATH/data/admin_path.pl ];then
            auth_path=$(cat $TGKING_PATH/data/admin_path.pl)
        fi
	    
        if [ "$address" == "" ];then
            v4=$(python3 $TGKING_PATH/tools.py getServerIp 4)
            v6=$(python3 $TGKING_PATH/tools.py getServerIp 6)

            if [ "$v4" != "" ] && [ "$v6" != "" ]; then

                if [ ! -f $TGKING_PATH/data/ipv6.pl ];then
                    echo 'True' > $TGKING_PATH/data/ipv6.pl
                    tgking_stop
                    tgking_start
                fi

                address="TGKING-Panel-Url-Ipv4: http://$v4:$port$auth_path \nMW-Panel-Url-Ipv6: http://[$v6]:$port$auth_path"
            elif [ "$v4" != "" ]; then
                address="TGKING-Panel-Url: http://$v4:$port$auth_path"
            elif [ "$v6" != "" ]; then

                if [ ! -f $TGKING_PATH/data/ipv6.pl ];then
                    #  Need to restart ipv6 to take effect
                    echo 'True' > $TGKING_PATH/data/ipv6.pl
                    mw_stop
                    mw_start
                fi
                address="TGKING-Panel-Url: http://[$v6]:$port$auth_path"
            else
                address="TGKING-Panel-Url: http://you-network-ip:$port$auth_path"
            fi
        else
            address="TGKING-Panel-Url: http://$address:$port$auth_path"
        fi

        show_panel_ip="$port|"
        echo -e "=================================================================="
        echo -e "\033[32mTGKING-Panel Default Info!\033[0m"
        echo -e "=================================================================="
        echo -e "$address"
        echo -e `python3 $TGKING_PATH/tools.py username`
        echo -e `python3 $TGKING_PATH/tools.py password`
        # echo -e "password: $password"
        echo -e "\033[33mWarning:\033[0m"
        echo -e "\033[33mIf you cannot access the panel. \033[0m"
        echo -e "\033[33mrelease the following port (${show_panel_ip}|80) in the security group.\033[0m"
        echo -e "=================================================================="
        ;;
    *)
        cd $mw_path && python3 $mw_path/tools.py cli $1
        ;;
esac
