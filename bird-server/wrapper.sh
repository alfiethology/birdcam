#!/bin/bash
#while true
# do
if ! pgrep -f 'pipeline.py'
then
python3 /home/pi/birdcam/bird-server/pipeline.py
#break
else
echo "pipeline.py already running"
#break
fi
#done

