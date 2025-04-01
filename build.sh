#!/bin/bash
apt-get update
apt-get install -y wget unzip xvfb libxi6 libgconf-2-4 libnss3 libxss1 libappindicator1 libindicator7 libgtk-3-0
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install
wget -N https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver
pip install -r requirements.txt
