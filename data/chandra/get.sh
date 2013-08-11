#!/bin/sh


URL="http://cxc.harvard.edu/target_lists/stscheds/"
curl --silent ${URL}oldscheds.html > chandra.html


STRIP_HTML="s/<[^>]*>//g"

NEW_FORMAT="sed -e ${STRIP_HTML} "
date
for FILE in `grep "^<A HREF" chandra.html | cut -d'"' -f2`
do
  echo "${FILE} \c"
  [ ${FILE} = "stschedAPR1311A.html" ]  && NEW_FORMAT="cat" && echo "\nSwitching to Old format"
  [ ! -s "${FILE}.gz" ] && echo "\nGetting ${FILE}" && curl --silent ${URL}${FILE} | ${NEW_FORMAT} | sed -e "/^$/d" | tail -n+4 > ${FILE} && gzip ${FILE}
done

echo ""
date

exit 0
