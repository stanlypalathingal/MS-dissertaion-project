#!/bin/bash

mg=$(docker run -d --name mongo --ip 172.17.0.2 ivanmarban/armhf-mongodb)
echo $mg
sleep 3
#exp=$(docker run -d --rm --name mongoexpress --ip 172.17.0.3 -p 8081:8081 --link mongo ind3x/rpi-mongo-express)
#echo $exp
sleep 1
brk=$(docker run -d --name mqttbroker -p 1883:1883 -p 9001:9001 eclipse-mosquitto)
echo $brk
sleep 2
jv=$(docker run -d --name java --ip 172.17.0.4 ashokjjk/benchmark:decrypt $1 192.168.2.106 --spring.data.mongodb.host=172.17.0.2)
echo $jv
sleep 3
py=$(docker run -d --name python --ip 172.17.0.5 stanlysac/edc:publish $1 192.168.2.106 $2)
echo $py
sleep 2
ml=$(docker run -d --name mlaccuracy --ip 172.17.0.6 stanlysac/edc:ml_pi  192.168.2.106 172.17.0.2)
echo $ml



