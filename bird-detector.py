from ultralytics import YOLO
import cv2
import os
import csv
import re
from pathlib import Path

# Load the YOLOv11x model
model = YOLO('/home/or22503/yolo11x.pt')  # Update with actual path to the model

# Path to video directory and CSV file
video_dir = Path('/media/or22503/birdcam_drive/Data')
csv_file = Path('/home/or22503/birdcam/bird_data.csv')

def extract_video_info(video_path):
    """Extract date, camera name, and time from the video filename."""
    match = re.search(r'(?P<date>\d{4}-\d{2}-\d{2})/(?P<camera>[^/]+)/(?P<time>\d{2}_\d{2}_\d{2})\.mp4$', str(video_path))
    if match:
        return match.group('date'), match.group('time').replace('_', ':')
    return None, None

def process_video(video_path):
    """Process a video file and return detected species as a set."""
    detected_species = set()
    cap = cv2.VideoCapture(str(video_path))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        results = model(frame, conf=0.8, imgsz=640)  # Set inference size to 640x640
        
        for r in results:
            for box in r.boxes:
                cls = model.names[int(box.cls[0])]  # Get detected class name
                detected_species.add(cls)
        
        if detected_species:
            break  # Stop processing after detecting at least one species
    
    cap.release()
    return detected_species

def write_to_csv(data):
    """Append unique detections to the CSV file."""
    file_exists = csv_file.exists()
    
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['species', 'date', 'time'])  # Write headers if file is new
        writer.writerows(data)

def main():
    """Iterate through videos and log detected species."""
    for video_path in video_dir.rglob('*.mp4'):
        date, time = extract_video_info(video_path)
        if not date or not time:
            continue
        
        detected_species = process_video(video_path)
        if detected_species:
            write_to_csv([[species, date, time] for species in detected_species])

if __name__ == "__main__":
    main()
