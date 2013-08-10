#!/bin/sh

COUNT=14
MAX=2504

cd `dirname $0`
echo "Satellite:  integral"
echo "Source:     http://xmm.esac.esa.int/"
echo "Data:       "`pwd`
date

curl --silent "http://xmm2.esac.esa.int/external/xmm_sched/sched_obs_srch_frame.shtml" > xmm-newton.html
# Can't get MAX, it's javascript. Need to find a better way
echo "Current revolution is ${MAX}"

while [ ${COUNT} -le ${MAX} ] 
do
  NUM=`echo ${COUNT} | awk '{printf("%04d",$1)}'`
  echo "${NUM} \c"

  [ ! -s "${NUM}.html.gz" ] && echo "\nGetting ${NUM}" && curl --silent http://xmm2.esac.esa.int/user/mplan/summaries/${NUM}_nice.html > ${NUM}.html && gzip ${NUM}.html
  COUNT=`expr ${COUNT} + 1`
done
echo ""
date

exit 0
