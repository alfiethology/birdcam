#!/usr/bin/env python3

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from datetime import datetime
from camera_settings import *
import os
import time
import libcamera
from gpiozero import MotionSensor

def record(camera_id):
    try:
        if camera_id in ['0', '1']:
            camera = Picamera2(int(camera_id))  # Load camera
            video_config = camera.create_video_configuration(
                main={"size": var_resolution}, controls={"FrameRate": var_framerate}
            )
            if var_vflip:
                video_config["transform"] = libcamera.Transform(hflip=1, vflip=1)
            camera.configure(video_config)
            encoder = H264Encoder()

        # Get device ID and timestamp
        device_id = os.uname()[1]
        dt = datetime.now()
        str_dt = dt.strftime("%Y_%m_%d-%H_%M_%S")
        datetag = dt.strftime("%Y_%m_%d")

        # Define output path
        output_path = os.path.join(var_out_folder, f"{device_id}_{datetag}")
        if var_record_external and var_external_paths:
            for path in var_external_paths:
                if os.path.exists(path):
                    output_path = os.path.join(path, f"{device_id}_{datetag}")

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
            
            # Properly close and release the camera
            camera.close()
            del camera  # Ensure the object is fully deleted

        elif camera_id == 'usb':
            command_record = (
                f'ffmpeg -t {var_length} -f v4l2 -framerate {var_framerate} "
                f'-video_size {var_resolution[0]}x{var_resolution[1]} -i {var_usb_device} {tmp_path}'
            )
            print(f'Starting to record {tmp_path}')
            os.system(command_record)
            print(f'Finished recording {tmp_path}')

        # Move the file to final output directory
        os.rename(tmp_path, out_path)

        # Ensure file is not lost if drive is removed unsafely
        if var_record_external and var_external_paths:
            lock_file = os.path.join(output_path, 'hack.lock')
            os.system(f"rm {lock_file} 2>/dev/null")
            os.system(f"touch {lock_file}")
            os.system(f"rm {lock_file}")

    except Exception as e:
        print(f"Error while recording: {e}")

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
            pir = MotionSensor(var_pir_gpio)
            print("Waiting for motion...")
            
            while True:
                pir.wait_for_motion()
                print("Motion detected, recording...")
                record(args.camera)
                print("Recording complete. Waiting for next motion...")
                
                time.sleep(2)  # Add a small delay to prevent immediate re-triggering

        finally:
            os.system(f"rm {lock_path}")

if __name__ == '__main__':
    main()
