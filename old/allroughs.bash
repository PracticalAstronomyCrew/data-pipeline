#!/bin/bash/

for DAILY in `seq 190415 190630`;
do
    DIR=/net/vega/data/users/observatory/images/$DAILY
    if [ -d "$DIR" ]; then
	echo "$DAILY data present"
	rm ~/rough/*$DAILY*
	python ~/code/observing/roughstats.py $DAILY
    fi
done

