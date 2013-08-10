#!/bin/sh

# Detailed data at http://heasarc.gsfc.nasa.gov/docs/xte/SOF/sts/Wk100.txt
# ../sts/Wk000.txt to ../sts/Wk831.txt

cd `dirname $0`
echo "Satellite:  RXTE"
echo "Source:     http://heasarc.gsfc.nasa.gov/docs/xte/xtegof.html"
echo "Data:       "`pwd`
date

COUNT="1"
MAX=831
while [ ${COUNT} -le ${MAX} ]
do
  NUM=`echo ${COUNT} | awk '{printf("%03d",$1)}'`
  echo "${NUM} \c"

  OUTPUT="rxte.${NUM}.txt"
  [ ! -f "${OUTPUT}.gz" ] && echo "\nGetting ${NUM}" && curl --silent http://heasarc.gsfc.nasa.gov/docs/xte/SOF/sts/Wk${NUM}.txt > ${OUTPUT} && gzip ${OUTPUT}
  COUNT=`expr ${COUNT} + 1`
done
echo ""
date

zcat rxte.*.txt.gz | awk -f rxte.awk > rxte.txt
gzip rxte.txt
