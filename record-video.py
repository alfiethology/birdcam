#!/usr/bin/env python3

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from datetime import datetime
from camera_settings import *
import os
import time
import libcamera
from gpiozero import MotionSensor  # Import MotionSensor for NIR motion detection

def record(camera_id):
    if camera_id == '0' or camera_id == '1':
        camera = Picamera2(int(camera_id))  # Load camera
        video_config = camera.create_video_configuration(
            main={"size": var_resolution}, controls={"FrameRate": var_framerate}
        )
        if var_vflip:
            video_config["transform"] = libcamera.Transform(hflip=1, vflip=1)
        camera.configure(video_config)
        encoder = H264Encoder()

    # Get device ID (hostname)
    device_id = os.uname()[1]
    # Get timestamp
    dt = datetime.now()
    str_dt = dt.strftime("%Y_%m_%d-%H_%M_%S")
    
    # Define output path
    datetag = dt.strftime("%Y_%m_%d")
    output_path = os.path.join(var_out_folder, device_id + '_' + datetag)
    
    # Check for external storage
    if var_record_external and var_external_paths:
        for path in var_external_paths:
            if os.path.exists(path):
                output_path = os.path.join(path, device_id + '_' + datetag)
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Construct filename
    filename = f"{device_id}_cam{camera_id}_{str_dt}.mp4"
    tmp_path = os.path.join('/tmp', filename)
    out_path = os.path.join(output_path, filename)

    if camera_id in ['0', '1']:
        # Use FfmpegOutput for recording
        mp4_path = FfmpegOutput(tmp_path)
        print(f'Starting to record {tmp_path}')
        
        if var_preview:
            camera.start_preview(Preview.QTGL)
            
        camera.start_recording(encoder, mp4_path)
        time.sleep(var_length)  # Record for 20 seconds
        camera.stop_recording()
        
        if var_preview:
            camera.stop_preview()
            
        print(f'Finished recording {tmp_path}')
    
    elif camera_id == 'usb':
        # Record via ffmpeg for USB camera
        command_record = (
            f'ffmpeg -t {var_length} -f v4l2 -framerate {var_framerate} '
            f'-video_size {var_resolution[0]}x{var_resolution[1]} -i {var_usb_device} {tmp_path}'
        )
        print(f'Starting to record {tmp_path}')
        os.system(command_record)
        print(f'Finished recording {tmp_path}')

    # Move to final output directory
    os.rename(tmp_path, out_path)

    # Ensure file isn't lost if drive is removed unsafely
    if var_record_external and var_external_paths:
        lock_file = os.path.join(output_path, 'hack.lock')
        os.system(f"rm {lock_file} 2>/dev/null")
        os.system(f"touch {lock_file}")
        os.system(f"rm {lock_file}")

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--camera", help="Camera ID")
    args = parser.parse_args()

    lock_path = f"/tmp/camjob{args.camera}.lock"

    if os.path.exists(lock_path):
        print("Recording is already in progress... exiting")
    else:
        os.system(f"touch {lock_path}")
        try:
            if var_pir:
                pir = MotionSensor(var_pir_gpio)
                print("Waiting for motion...")
                pir.wait_for_motion()  # Wait until motion is detected
                print("Motion detected, recording...")
                record(args.camera)
            else:
                record(args.camera)
        finally:
            os.system(f"rm {lock_path}")

if __name__ == '__main__':
    main()
