#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
# LANG=en_US.UTF-8
is64bit=`getconf LONG_BIT`

startTime=`date +%s`

_os=`uname`
echo "use system: ${_os}"

if [ "$EUID" -ne 0 ]
  then echo "Please run as root!"
  exit
fi

{

if [ ${_os} == "Darwin" ]; then
	OSNAME='macos'
elif grep -Eqi "openSUSE" /etc/*-release; then
	OSNAME='opensuse'
	zypper refresh
elif grep -Eqi "FreeBSD" /etc/*-release; then
	OSNAME='freebsd'
elif grep -Eqi "CentOS" /etc/issue || grep -Eqi "CentOS" /etc/*-release; then
	OSNAME='centos'
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
	apt install -y wget zip unzip
elif grep -Eqi "Ubuntu" /etc/issue || grep -Eqi "Ubuntu" /etc/*-release; then
	OSNAME='ubuntu'
	apt install -y wget zip unzip
elif grep -Eqi "Raspbian" /etc/issue || grep -Eqi "Raspbian" /etc/*-release; then
	OSNAME='raspbian'
else
	OSNAME='unknow'
fi

# cn=$(curl -fsSL -m 10 http://ipinfo.io/json | grep "\"country\": \"CN\"")
HTTP_PREFIX="https://"
LOCAL_ADDR=common
ping  -c 1 github.com > /dev/null 2>&1
if [ "$?" != "0" ];then
	LOCAL_ADDR=cn
	HTTP_PREFIX="https://ghproxy.com/"
fi

CP_CMD=/usr/bin/cp
if [ -f /bin/cp ];then
		CP_CMD=/bin/cp
fi

echo "update tg-king code start"


curl --insecure -sSLo /tmp/dev.zip https://github.com/midoks/tg-king/archive/refs/heads/dev.zip
cd /tmp && unzip /tmp/dev.zip
$CP_CMD -rf /tmp/tg-king-dev/* /opt/tg-king
rm -rf /tmp/dev.zip
rm -rf /tmp/tg-king-dev

echo "update tg-king code end"

rm -rf /tmp/dev.zip
rm -rf /tmp/tg-king-dev

#pip uninstall public
echo "use system version: ${OSNAME}"
cd /opt/tg-king && bash scripts/update/${OSNAME}.sh

bash /etc/rc.d/init.d/tgking restart
bash /etc/rc.d/init.d/tgking default

if [ -f /usr/bin/mw ];then
	rm -rf /usr/bin/mw
fi

if [ ! -e /usr/bin/mw ]; then
	if [ ! -f /usr/bin/mw ];then
		ln -s /etc/rc.d/init.d/mw /usr/bin/mw
	fi
fi

endTime=`date +%s`
((outTime=($endTime-$startTime)/60))
echo -e "Time consumed:\033[32m $outTime \033[0mMinute!"

} 1> >(tee /www/server/mdserver-web/logs/tgking-update.log) 2>&1