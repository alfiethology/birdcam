from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import argparse

app = Flask(__name__)
def generate_frames():
    while True:
        frame = camera.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/video_feed')

def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-W", "--width", default = 640, type = int, help="Video width in pixels")
    parser.add_argument("-H", "--height", default = 360, type = int, help="Video height in pixels")
    args = parser.parse_args()
    # set up camera
    camera = Picamera2()
    camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (args.width, args.height)}))
    camera.start()
    # start app
    app.run(host='0.0.0.0', port=5000)
