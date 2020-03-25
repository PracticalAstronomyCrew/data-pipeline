#!/bin/bash/
SHEETS=~/public_html/obs/sheets/sheets.html
rm $SHEETS
echo "<html><body>" > $SHEETS
LATEST=0
#for DAILY in `seq 191231 -1 001231`;
for DAILY in {201213..080506};
do
    DIR=/net/vega/data/users/observatory/images/$DAILY
    if [ -d "$DIR" ]; then
	if ! [ -f ~/public_html/obs/sheets/OBSSHEET_$DAILY.txt ]; then
	    echo "$DAILY data present -- processing"
	    python ~/code/observing/obssheet.py $DAILY
	    mv OBSSHEET_$DAILY.txt ~/public_html/obs/sheets/
	else
	    echo "$DAILY data present -- Already Done"
	fi
	echo "$DAILY <a href=\"https://www.astro.rug.nl/~noelstorr/obs/sheets/OBSSHEET_$DAILY.txt\" target="_new">https://www.astro.rug.nl/~noelstorr/obs/sheets/OBSSHEET_$DAILY.txt</a><br>" >> $SHEETS
	if [ $DAILY -gt $LATEST ]; then LATEST=$DAILY; fi
    fi
done
echo "</body></html>" >> $SHEETS

echo "Last Night is $LATEST"
	if ! [ -f ~/rough/processed$LATEST.txt ]; then
	    echo "Processing Attempted $LATEST" > ~/rough/processed$LATEST.txt
	    echo "Rough Stats for New Data $LATEST"
	    python ~/code/observing/roughstats.py $LATEST
	    mv ROUGHSTATS_$LATEST.txt ~/public_html/obs/latest_rough.txt
	    mail -s "New Data Recorded for $LATEST" newdata.bn8k04@zapiermail.com <<< "$LATEST"
	    echo "Processing Concluded $LATEST" >> ~/rough/processed$LATEST.txt
	fi
