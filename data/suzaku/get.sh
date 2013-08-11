#!/bin/sh

URL="http://www.astro.isas.ac.jp/suzaku/schedule/shortterm/"
curl --silent ${URL} > suzaku.html

for FILE in `grep "<LI>" suzaku.html | cut -d'"' -f2`
do
  HTML=`basename ${FILE}`
  echo $FILE $HTML
  [ ! -s "${HTML}.gz" ] && echo "\nGetting ${HTML}" && curl --silent ${URL}${FILE} > ${HTML} && gzip ${HTML}
done
