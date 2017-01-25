#!/bin/bash
echo "upload all the testSerial.py to neurons 1 to 20 and all the muscles"
echo "+++++++++++++++++++++++++++++++++++++++"
date
echo "+++++++++++++++++++++++++++++++++++++++"
echo " Uploading to neurons 1 to 20 ... "
for I in {1..20}
do
	echo "100.100.0.$I"
	sshpass -p 'sielegans2013' scp testSerial.py pedro@100.100.0.$I:/home/pedro/MC
done
echo "++++++++++++++++++++++++++++++++++++++"
date
echo "++++++++++++++++++++++++++++++++++++++"
echo "Uploading to all the muscles ..."
for J in {47..73}
do
	echo "100.100.1.$J"
	sshpass -p 'sielegans2013' scp testSerial.py pedro@100.100.1.$J:/home/pedro/MC
done
echo "++++++++++++++++++++++++++++++++++++++"
date
echo "++++++++++++++++++++++++++++++++++++++"
echo "Update complete!"
