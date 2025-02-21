# Bird Feeder Monitoring System

This guide provides setup instructions for a bird feeder monitoring system using Raspberry Pi devices, a PIR sensor, and a camera. The system consists of three components:  

1. **bird-server** – Handles video collection and management.  
2. **bird-monitor** – Runs on a camera-equipped Raspberry Pi with a PIR sensor to detect and record bird activity.  
3. **bird-detector** – Runs on a desktop with CUDA-enabled GPU for species detection using YOLO.  

---

## 📌 You Will Need  
- **2 x Raspberry Pi** (Zero, 4, or 5) with Raspbian OS installed.  
- **Camera module** for the Raspberry Pi camera unit.  
- **PIR Sensor** for motion detection.  

### 🔗 PIR Sensor Installation  
Installation instructions for a standard PIR sensor:  
👉 [Arduino PIR Sensor Troubleshooting & Sensitivity Adjustment](https://support.arduino.cc/hc/en-us/articles/4403050020114-Troubleshooting-PIR-Sensor-and-sensitivity-adjustment)  

### 🛠 PIR Sensor Wiring  
- **5V Output Cable** → **Pin 2**  
- **Output Cable** → **Pin 11**  
- **Ground** → **Pin 9**  

This setup worked for me; check the above link for pin variations.  

### 🔗 Clone the Repository  
Clone the project repository into the home directory on **both** the **server Pi** and the **camera Pi**:  
```bash
git clone <repository_url> ~/birdcam
```

---

## 📂 bird-server (Raspberry Pi Server)  

The **bird-server** component fetches videos from camera units and stores them on a mounted external drive.  

### ⚙️ Configuration  

1. **Set Camera IPs**  
   - Open `bird-server/fetch_settings.py` and modify:  
     ```python
     client_list = ["<camera_pi_IP_1>", "<camera_pi_IP_2>"]
     ```
2. **Mount External Drive**  
   - Follow instructions in `bird-server/mounting_instructions.md`.  
   - Create a **Data** folder on the mounted drive:  
     ```bash
     mkdir /mnt/<your_drive>/Data
     ```
   - Create a **health check file**:  
     ```bash
     touch /mnt/<your_drive>/hello.check
     ```
   - Add the drive path to `fetch_settings.py`:  
     ```python
     ext_checks = "/mnt/<your_drive>/hello.check"
     ```

3. **Modify Wrapper Script**  
   - Edit `bird-server/wrapper.sh` to set the correct path to `pipeline.py`.  
   - Default assumes username `pi = pi`.  

### ⏲ Automate Data Fetching with Cron  
Edit crontab:  
```bash
crontab -e
```
If prompted, select option **1** for the default editor.  

Add the following line to execute `pipeline.py` every minute:  
```bash
* * * * * /home/pi/birdcam/bird-server/pipeline.py
```
💡 Adjust timing as needed if you don't want data fetching to run every minute.  

---

## 🎥 bird-monitor (Camera Unit with PIR Sensor)  

The **bird-monitor** component runs on the Raspberry Pi camera unit. It detects movement and records video.  

### ⏲ Automate Video Recording with Cron  
Edit crontab:  
```bash
crontab -e
```
Add the following line to execute `wrapper.sh` every minute:  
```bash
* * * * * /home/pi/birdcam/bird-monitor/wrapper.sh
```
The wrapper script ensures that the recording script runs only if it's not already active.  

---

## 🖥 bird-detector (Desktop with CUDA + GPU)  

The **bird-detector** runs on a desktop computer with **CUDA-enabled GPU** and **YOLO** for species detection.  

### ⚙️ Configuration  

1. **Set YOLO Model Path**  
   - Modify `bird-detector/detect.py`, line **9**:  
     ```python
     yolo_model = "<path_to_your_YOLO_model>"
     ```
   - Alternatively, download a YOLO model from the official site:  
     👉 [YOLO Object Detection](https://docs.ultralytics.com/tasks/detect/)  

2. **Set Video Input Path**  
   - Modify line **12** to specify the mounted drive where videos are stored:  
     ```python
     video_path = "/mnt/<your_drive>/Data"
     ```

3. **Set CSV Output Path**  
   - Modify line **13** to set the path where detected species data will be stored:  
     ```python
     csv_output = "/mnt/<your_drive>/species_data.csv"
     ```

4. **Plotting Species Data**  
   - A simple **R script** in `bird-detector` generates a visualization of which species are seen at different times.  

---

## 🎯 Summary  

| Component       | Function                                   |
|---------------|--------------------------------|
| **bird-server**  | Collects & stores video from camera units. |
| **bird-monitor** | Detects motion & records video.         |
| **bird-detector** | Identifies species using YOLO & logs data. |

This system allows automated detection, recording, and species tracking at your bird feeder! 🐦📷🚀  
```
