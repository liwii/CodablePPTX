#!/bin/sh

fswatch -0 ./ | while read -d "" event
do
  E=${event}
  EXT=${E##*.}
  FILE=${E##*/}
  if test $EXT = "yaml" || test $EXT = "yml"; then
    echo $FILE changed
    python presentation.py $1 $2
    soffice --headless --convert-to pdf $2
    BASE=$2
    md5sum ${BASE%.*}.pdf > ${BASE%.*}.md5
    echo $2 generated
  fi
done