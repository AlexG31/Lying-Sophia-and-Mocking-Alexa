#!/bin/sh -x
user='gpf'
nginx_config=$1
sudo docker run --name nginx-alexa \
 -v $nginx_config:/etc/nginx/nginx.conf:ro \
 -v "/home/$user/:/home/alexg/" \
 -p 80:9002 \
 -d nginx
