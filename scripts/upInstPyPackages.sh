#!/bin/bash
echo "update all the threadsDef.py in neurons 1 to 20 and muscles"
echo "+++++++++++++++++++++++++++++++++++++++"
date
echo "+++++++++++++++++++++++++++++++++++++++"
echo " Updating neurons 1 to 20 ... "

for I in {1..255}
do
	echo "+++++++++++++++++++++++++++++++++++++++"
	echo "100.100.0.$I"
	echo "+++++++++++++++++++++++++++++++++++++++"
	sshpass -p 'sielegans2013' ssh pedro@100.100.0.$I rm run.sh
	sshpass -p 'sielegans2013' ssh pedro@100.100.0.$I rm instPyPackages.sh
	sshpass -p 'sielegans2013' scp instPyPackages.sh pedro@100.100.0.$I:/home/pedro/
	sshpass -p 'sielegans2013' scp update.sh pedro@100.100.0.$I:/home/pedro/
	sshpass -p 'sielegans2013' scp run.sh pedro@100.100.0.$I:/home/pedro/
	sshpass -p 'sielegans2013' ssh pedro@100.100.0.$I ./instPyPackages.sh
done

for I in {0..119}
do
	echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	echo "100.100.1.$I"
	echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	sshpass -p 'sielegans2013' ssh pedro@100.100.1.$I rm run.sh
	sshpass -p 'sielegans2013' ssh pedro@100.100.1.$I rm instPyPackages.sh
	sshpass -p 'sielegans2013' scp instPyPackages.sh pedro@100.100.1.$I:/home/pedro/
	sshpass -p 'sielegans2013' scp update.sh pedro@100.100.1.$I:/home/pedro/
	sshpass -p 'sielegans2013' scp run.sh pedro@100.100.1.$I:/home/pedro/
	sshpass -p 'sielegans2013' ssh pedro@100.100.1.$I ./instPyPackages.sh
done
echo "++++++++++++++++++++++++++++++++++++++"
date
echo "++++++++++++++++++++++++++++++++++++++"
echo "Update complete!"
