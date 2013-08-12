#!/bin/sh

SCRIPT_NAME=`basename $0 | sed -e "s/\.sh$//"`
[ -z "${TMP_DIR}" ] && TMP_DIR="/tmp"
TMP_FILE="${TMP_DIR}/${SCRIPT_NAME}.tmp.$$"

DATA_DIR=`dirname $0`

FILE="${DATA_DIR}/data.txt.gz"
echo "Processing ${FILE}..."
zcat ${FILE} > ${TMP_FILE}
python admin/scripts/spitzer.py ${TMP_FILE}

rm -f ${TMP_FILE}*
exit 0
