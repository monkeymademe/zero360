#!/bin/sh
# launcher.sh
# navigate to home directory then execute python script
# sudo crontab -e
# @reboot sh /home/pi/launcher.sh >/home/pi/logs/cronlog 2>&1
# mkdir logs

cd /home/pi/
python node.py
