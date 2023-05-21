#!/bin/sh
a='1,2'
a1=(${a//,/ })
a2=($a1)

for var in ${a1[@]}
do
  echo $var
done 

echo $a

