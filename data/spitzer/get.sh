#!/bin/sh

#curl --silent http://irsa.ipac.caltech.edu/data/SPITZER/docs/files/spitzer/spitzer_obslog.txt > spitzer.txt
head -32 spitzer.txt > index.txt
tail -n+33 spitzer.txt | grep -v "^earth" | grep -v "^none"  | grep -v "^Comment" | grep -v "^End of" | sed  -e "/^   .*$/d;/^$/d;/^ $/d" > data.txt
#gzip data.txt
