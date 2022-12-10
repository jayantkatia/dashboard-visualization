#!/bin/bash

# IMPORTANT
# Edit values starting with CHANGE_
# Do not edit values starting with YOUR_

## install
sudo apt update
sudo apt install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install -y python3-venv

## create virtual env and install requirements
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate


## create and start a service
sudo cp dashboard.service /etc/systemd/system/dashboard.service
sudo sed -i 's/YOUR_USERNAME/CHANGE_USERNAME/g' /etc/systemd/system/dashboard.service
sudo sed -i 's/YOUR_PROJECT_FOLDER/CHANGE_PROJECT_FOLDER/g' /etc/systemd/system/dashboard.service
sudo systemctl start dashboard
sudo systemctl enable dashboard

## install nginx and certbot
sudo apt install nginx
sudo ln -s /etc/nginx/sites-available /etc/nginx/sites-enabled

sudo apt install -y python3 python3-venv libaugeas0
sudo python3 -m venv /opt/certbot/
sudo /opt/certbot/bin/pip install --upgrade pip
sudo /opt/certbot/bin/pip install certbot certbot-nginx
sudo ln -s /opt/certbot/bin/certbot /usr/bin/certbot
sudo certbot certonly --nginx -d CHANGE_DOMAIN_HERE -m CHANGE_EMAIL --agree-tos -n

## editing nginx conf
sudo cp nginx/default /etc/nginx/sites-available/
sudo sed -i 's/YOUR_USERNAME/CHANGE_USERNAME/g' /etc/nginx/sites-available/default
sudo sed -i 's/YOUR_PROJECT_FOLDER/CHANGE_PROJECT_FOLDER/g' /etc/nginx/sites-available/default
sudo sed -i 's/YOUR_DOMAIN/CHANGE_DOMAIN/g' /etc/nginx/sites-available/default

sudo nginx -t
sudo systemctl restart nginx

## cron job for certificatte renewal
echo "0 0,12 * * * root /opt/certbot/bin/python -c 'import random; import time; time.sleep(random.random() * 3600)' && sudo certbot renew -q" | sudo tee -a /etc/crontab > /dev/null
