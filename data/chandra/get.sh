#!/bin/sh

TMP_FILE="/tmp/chandra.tmp.$$"

URL="http://cxc.harvard.edu/target_lists/stscheds/"
curl --silent ${URL}oldscheds.html > chandra.html

cd `dirname $0`
echo "Satellite:  Chandra"
echo "Source:     http://cxc.harvard.edu/target_lists/stscheds/"
echo "Data:       "`pwd`
date


STRIP_HTML="s/<[^>]*>//g"

NEW_FORMAT="Y"
date
for FILE in `grep "^<A HREF" chandra.html | cut -d'"' -f2`
do
  echo "${FILE} \c"
  [ ${FILE} = "stschedAPR1311A.html" ]  && OLD_FORMAT="Y" && NEW_FORMAT=""
  if [ ! -s "${FILE}.gz" ] 
  then
    echo "\nGetting ${FILE} \c" 
    curl --silent ${URL}${FILE} > ${TMP_FILE} 
    if [ ! -z "${NEW_FORMAT}" ]
    then
      sed -e ${STRIP_HTML} ${TMP_FILE} | sed -e "/^$/d" | tail -n+4 | grep -v "^ ---- " > ${FILE} 
    else 
      mv ${TMP_FILE} ${FILE}
    fi
    LINES=`cat ${FILE} | wc -l`
    echo "(${LINES})"
    gzip ${FILE}
  fi
done

echo ""
date

rm -f ${TMP_FILE}
exit 0
