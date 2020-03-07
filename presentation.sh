#!/bin/sh
while true
do
python presentation.py $1 $2
soffice --headless --convert-to pdf $2
BASE=$2
md5sum ${BASE%.*}.pdf > ${BASE%.*}.md5
sleep 5
done

