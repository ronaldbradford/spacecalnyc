#!/bin/sh


START="2005-06-04"
TODAY=`date +%Y-%m-%d`


cd `dirname $0`
echo "Satellite:  Swift"
echo "Source:     https://www.swift.psu.edu/operations/obsSchedule.php"
echo "Data:       "`pwd`
date

DATE=${START}
while [ "${DATE}" != "${TODAY}" ]
do
  echo "${DATE} \c"
  [ ! -s "${DATE}.html.gz" ] && echo "\nGetting ${DATE}" && curl --silent "https://www.swift.psu.edu/operations/obsSchedule.php?d=${DATE}&a=0" > ${DATE}.html && gzip ${DATE}.html
  DATE=`date +%Y-%m-%d -d "$DATE 1 day"`
done

echo ""
date


