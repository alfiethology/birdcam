#!/bin/bash
#while true
# do
if ! pgrep -f 'record-video.py'
then
python /home/pi/birdcam/record-video.py -c '0'
#break
else
echo "record-video.py already running"
#break
fi
#done

