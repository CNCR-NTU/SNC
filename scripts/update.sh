#! /bin/bash
echo "sielegans2013" | sudo -S apt clean
sudo apt -y autoremove
echo "sielegans2013" | sudo -S apt update
sudo apt -y upgrade
echo "sielegans2013" | sudo -S apt dist-upgrade
echo "sielegans2013" | sudo -S apt autoremove
sudo reboot
