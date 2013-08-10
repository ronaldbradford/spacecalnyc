#!/bin/sh

COUNT=10


cd `dirname $0`
echo "Satellite:  integral"
echo "Source:     http://integral.esac.esa.int/isocweb"
echo "Data:       "`pwd`
date

curl --silent "http://integral.esac.esa.int/isocweb/schedule.html?action=intro" > integral.htm
MAX=`grep "Current revolution" integral.htm | sed -e"s/^.*endRevno=//" | cut -d'"' -f1`
[ -z "${MAX}" ] && echo "ERROR: Unable to obtain current revolution" && exit 1
echo "Current revolution is ${MAX}"

while [ ${COUNT} -le ${MAX} ] 
do
  NUM=`echo ${COUNT} | awk '{printf("%04d",$1)}'`
  echo "${NUM} \c"

  #Search on Count
  [ ! -s "${NUM}.csv.gz" ] && echo "\nGetting ${NUM}" && curl --silent "http://integral.esac.esa.int/isocweb/schedule.html?action=schedule&startRevno=${COUNT}&endRevno=${COUNT}&reverseSort=&format=csv"  | grep -v "^\"Rev"> ${NUM}.csv && gzip ${NUM}.csv
  COUNT=`expr ${COUNT} + 1`
done
echo ""
date

exit 0
