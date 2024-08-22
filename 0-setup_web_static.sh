#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment
# web_static.

sudo apt-get -y update
sudo apt-get install -y nginx

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
ln -sf /data/web_static/releases/test/ /data/web_static/current
echo "Hello people!" > /data/web_static/releases/test/index.html
sudo chown -R ubuntu:ubuntu /data/
printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root    /var/www/html;
    index   index.html index.htm index.nginx-debian.html;

    server_name _;

    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html index.htm;
        autoindex off;
    }
    location /redirect_me {
        return 301 http://juliusdgenius.tech;
    }

    error+page 404 /404.html;
    location /404 {
        root /var/www/error;
        internal;
    }
}" > /etc/nginx/sites-available/default
sudo service nginx restart
