#!/bin/bash
echo "update all the threadsDef.py in neurons 1 to 20 and muscles"
echo "+++++++++++++++++++++++++++++++++++++++"
date
echo "+++++++++++++++++++++++++++++++++++++++"
echo " Updating neurons 1 to 375 ... "

for I in {1..375}
do
	echo "+++++++++++++++++++++++++++++++++++++++"
	echo "100.100.0.$I"
	echo "+++++++++++++++++++++++++++++++++++++++"
#	sshpass -p 'sielegans2013' ssh pedro@n$i rm run.sh
	sshpass -p 'sielegans2013' ssh pedro@n$I rm instPyPackages.sh
	sshpass -p 'sielegans2013' scp instPyPackages.sh pedro@n$I:/home/pedro/
#	sshpass -p 'sielegans2013' scp update.sh pedro@100.100.0.$I:/home/pedro/
#	sshpass -p 'sielegans2013' scp run.sh pedro@100.100.0.$I:/home/pedro/
	sshpass -p 'sielegans2013' ssh pedro@n$I ./instPyPackages.sh
done
echo "++++++++++++++++++++++++++++++++++++++"
date
echo "++++++++++++++++++++++++++++++++++++++"
echo "Update complete!"
