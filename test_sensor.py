from gpiozero import MotionSensor
import time

# Define the PIR sensor
pir = MotionSensor(4)  # Change the GPIO pin if needed

try:
    print("Monitoring motion sensor. Press Ctrl+C to stop.")
    while True:
        if pir.motion_detected:
            print("Motion detected!")
        else:
            print("No motion detected.")
        time.sleep(0.5)  # Adjust the sleep time as needed

except KeyboardInterrupt:
    print("\nExiting...")
