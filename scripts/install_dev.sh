#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
# LANG=en_US.UTF-8
is64bit=`getconf LONG_BIT`

echo -e "You are installing\033[31m tg-king dev version\033[0m, normally use install.sh for production.\n" 
sleep 1

{

startTime=`date +%s`

_os=`uname`
echo "use system: ${_os}"

if [ "$EUID" -ne 0 ]
  then echo "Please run as root!"
  exit
fi


if [ ${_os} == "Darwin" ]; then
	OSNAME='macos'
elif grep -Eq "openSUSE" /etc/*-release; then
	OSNAME='opensuse'
	zypper refresh
elif grep -Eq "FreeBSD" /etc/*-release; then
	OSNAME='freebsd'
elif grep -Eqi "CentOS" /etc/issue || grep -Eqi "CentOS" /etc/*-release; then
	OSNAME='rhel'
	yum install -y wget zip unzip
elif grep -Eqi "Fedora" /etc/issue || grep -Eqi "Fedora" /etc/*-release; then
	OSNAME='rhel'
	yum install -y wget zip unzip
elif grep -Eqi "Rocky" /etc/issue || grep -Eqi "Rocky" /etc/*-release; then
	OSNAME='rhel'
	yum install -y wget zip unzip
elif grep -Eqi "AlmaLinux" /etc/issue || grep -Eqi "AlmaLinux" /etc/*-release; then
	OSNAME='rhel'
	yum install -y wget zip unzip
elif grep -Eqi "Amazon Linux" /etc/issue || grep -Eqi "Amazon Linux" /etc/*-release; then
	OSNAME='amazon'
	yum install -y wget zip unzip
elif grep -Eqi "Debian" /etc/issue || grep -Eqi "Debian" /etc/*-release; then
	OSNAME='debian'
	apt update -y
	apt install -y devscripts
	apt install -y wget zip unzip
elif grep -Eqi "Ubuntu" /etc/issue || grep -Eqi "Ubuntu" /etc/*-release; then
	OSNAME='ubuntu'
	apt install -y wget zip unzip
else
	OSNAME='unknow'
fi

echo "use system version: ${OSNAME}"

if [ ! -d /opt/tg-king ];then
	curl --insecure -sSLo /tmp/dev.zip https://github.com/midoks/tg-king/archive/refs/heads/dev.zip
	cd /tmp && unzip /tmp/dev.zip
	mv -f /tmp/tg-king-dev /opt/tg-king
	rm -rf /tmp/dev.zip
	rm -rf /tmp/tg-king-dev	
fi


HTTP_PREFIX="https://"
LOCAL_ADDR=common
ping -c 1 ipinfo.io > /dev/null 2>&1
if [ "$?" == "0" ];then
    CN=$(curl -fsSL -m 10 http://ipinfo.io/json | grep "\"country\": \"CN\"")
    if [ ! -z "$CN" ];then
        LOCAL_ADDR=cn
        HTTP_PREFIX="https://ghproxy.com/"
    fi
fi

PIPSRC="https://pypi.python.org/simple"
if [ "$LOCAL_ADDR" != "common" ];then
    PIPSRC="https://pypi.tuna.tsinghua.edu.cn/simple"
fi

echo "pypi source:$PIPSRC"
#面板需要的库
if [ ! -f /usr/local/bin/pip3 ] && [ ! -f /usr/bin/pip3 ];then
    python3 -m pip install --upgrade pip setuptools wheel -i $PIPSRC
fi

which pip && pip install --upgrade pip -i $PIPSRC
pip3 install --upgrade pip setuptools wheel -i $PIPSRC

cd /opt/tg-king && pip3 install -r /opt/tg-king/requirements.txt -i $PIPSRC

# pip3 install flask-caching==1.10.1
# pip3 install mysqlclient

if [ ! -f /opt/tg-king/bin/activate ];then
    cd /opt/tg-king && python3 -m venv .
    cd /opt/tg-king && source /opt/tg-king/bin/activate
else
    cd /opt/tg-king && source /opt/tg-king/bin/activate
fi

pip install --upgrade pip -i $PIPSRC
pip3 install --upgrade setuptools -i $PIPSRC
cd /opt/tg-king && pip3 install -r /opt/tg-king/requirements.txt -i $PIPSRC


cd /opt/tg-king && bash cli.sh start
isStart=`ps -ef|grep 'gunicorn -c setting.py apptg:app' |grep -v grep|awk '{print $2}'`
n=0
while [ ! -f /etc/rc.d/init.d/tgking ];
do
    echo -e ".\c"
    sleep 1
    let n+=1
    if [ $n -gt 20 ];then
    	echo -e "start tgking fail"
        exit 1
    fi
done

endTime=`date +%s`
((outTime=(${endTime}-${startTime})/60))
echo -e "Time consumed:\033[32m $outTime \033[0mMinute!"

} 1> >(tee tgking-install.log) 2>&1

echo -e "\nInstall completed. If error occurs, please contact us with the log file tgking-install.log ."

