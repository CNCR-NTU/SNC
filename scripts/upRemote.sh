#!/bin/bash
echo "update all the downloadManager.py in neurons 1 to 20 and muscles"
echo "+++++++++++++++++++++++++++++++++++++++"
date
echo "+++++++++++++++++++++++++++++++++++++++"
echo " Updating neuron platforms ... "
for I in {1..255}
do
	echo "100.100.0.$I"
	sshpass -p 'sielegans2013' scp update.sh pedro@100.100.0.$I:/home/pedro
done
echo "++++++++++++++++++++++++++++++++++++++"
date
echo "++++++++++++++++++++++++++++++++++++++"

for J in {0..119}
do
	echo "100.100.1.$J"
	sshpass -p 'sielegans2013' scp update.sh pedro@100.100.1.$J:/home/pedro
done
echo "++++++++++++++++++++++++++++++++++++++"
date
echo "++++++++++++++++++++++++++++++++++++++"
echo "Update complete!"
