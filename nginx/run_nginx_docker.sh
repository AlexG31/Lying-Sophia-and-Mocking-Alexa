#!/bin/sh -x
nginx_config=$1
sudo docker run --name nginx-l2 \
 -v $nginx_config:/etc/nginx/nginx.conf:ro \
 -v /home/alexg/:/home/alexg/ \
 -p 80:9002 \
 -d nginx
