#!/bin/sh



cd `dirname $0`
echo "Satellite:  Fermi"
echo "Source:     http://fermi.gsfc.nasa.gov/ssc/observations/timeline/posting/"
echo "Data:       "`pwd`
date

curl --silent "http://fermi.gsfc.nasa.gov/ssc/observations/timeline/posting/" > fermi.html
#MAX=`grep "Current revolution" integral.htm | sed -e"s/^.*endRevno=//" | cut -d'"' -f1`
MAX=5
[ -z "${MAX}" ] && echo "ERROR: Unable to obtain current revolution" && exit 1
#echo "Current revolution is ${MAX}"

COUNT=1
while [ ${COUNT} -le ${MAX} ] 
do
  NUM=${COUNT}
  echo "${NUM} \c"

  [ ! -s "${NUM}.csv.gz" ] && echo "\nGetting ${NUM}" && curl --silent "http://fermi.gsfc.nasa.gov/ssc/observations/timeline/posting/ao${NUM}/" > ${NUM}.html && gzip ${NUM}.html
  COUNT=`expr ${COUNT} + 1`
done
echo ""
date

exit 0
