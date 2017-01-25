#! /bin/bash
rm -rf SNC
git clone 
echo "sielegans2013" | sudo -S apt-get clean
sudo apt-get -y autoremove
echo "sielegans2013" | sudo -S apt-get update
sudo apt-get -y upgrade
echo "sielegans2013" | sudo -S apt-get dist-upgrade
echo "sielegans2013" | sudo -S apt-get autoremove
sudo reboot
