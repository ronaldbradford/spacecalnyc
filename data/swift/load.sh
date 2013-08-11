#!/bin/sh

SCRIPT_NAME=`basename $0 | sed -e "s/\.sh$//"`
[ -z "${TMP_DIR}" ] && TMP_DIR="/tmp"
TMP_FILE="${TMP_DIR}/${SCRIPT_NAME}.tmp.$$"

DATA_DIR=`dirname $0`
for FILE in `ls ${DATA_DIR}/*.gz`
do
  echo "Processing ${FILE}..."
  zcat ${FILE} > ${TMP_FILE}
  python admin/scripts/swift.py ${TMP_FILE}
done

rm -f ${TMP_FILE}*
exit 0
