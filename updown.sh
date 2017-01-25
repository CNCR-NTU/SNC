#!/bin/bash
echo "update all the downloadManager.py in neurons 1 to 20 and muscles"
echo "+++++++++++++++++++++++++++++++++++++++"
date
echo "+++++++++++++++++++++++++++++++++++++++"
echo " Updating neurons 1 to 20 ... "
for I in {1..20}
do
	echo "100.100.0.$I"
	sshpass -p 'sielegans2013' scp downloadManager.py pedro@100.100.0.$I:/home/pedro/MC
done
echo "++++++++++++++++++++++++++++++++++++++"
date
echo "++++++++++++++++++++++++++++++++++++++"
echo "Updating muscles ..."
for J in {47..73}
do
	echo "100.100.1.$J"
	sshpass -p 'sielegans2013' scp downloadManager.py pedro@100.100.1.$J:/home/pedro/MC
done
echo "++++++++++++++++++++++++++++++++++++++"
date
echo "++++++++++++++++++++++++++++++++++++++"
echo "Update complete!"
