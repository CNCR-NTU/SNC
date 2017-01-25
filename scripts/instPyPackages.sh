#! /bin/bash
echo "sielegans2013" | sudo -S apt-get update
sudo apt-get -y install python3-numpy python3-lxml python3-serial python3-requests ntp python3-bitstring python3-bitarray
rm -rf Ethernet_Blaster/
rm -rf minnow-max-extras/
rm -rf MC/
rm -rf pedro
rm -rf SNC
rm blink.py
git clone https://github.com/pedrombmachado/SNC.git
rm instPyPackages.sh
