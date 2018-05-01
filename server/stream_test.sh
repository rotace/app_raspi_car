#!/bin/bash
# ref: http://www.hiramine.com/physicalcomputing/raspberrypi/webcamstreaming.html

DIR="$HOME/workspace/mjpg-streamer/"

if pgrep mjpg_streamer > /dev/null
then
echo "mjpg_streamer already running"
else
cd $DIR
./mjpg_streamer -i "./input_uvc.so -f 10 -r 320x240 -d /dev/video0 -y -n" -o "./output_http.so -w ./www -p 9000"
cd -
fi
