#!/bin/bash
# ref: https://kitto-yakudatsu.com/archives/2338

DIR="/home/pi/workspace/mjpg-streamer/mjpg-streamer-experimental/"

if pgrep mjpg_streamer > /dev/null
then
echo "mjpg_streamer already running"
else
LD_LIBRARY_PATH=$DIR $DIR/mjpg_streamer -i "input_raspicam.so -fps 10 -q 20 -x 640 -y 480" -o "output_http.so -w ./www -p 9000"
fi
