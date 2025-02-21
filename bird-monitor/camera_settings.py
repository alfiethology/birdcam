import os

var_resolution = (1296, 972)  # Camera resolution
var_framerate = 30  # Framerate
var_vflip = True  # Vertical flip
var_length = 15  # Recording length in seconds (Updated for NIR sensor)
var_pir = True  # Enable motion sensor trigger (set to True)
var_pir_gpio = 17  # GPIO pin for NIR motion sensor
var_out_folder = '/home/pi/Data/'  # Output folder
var_preview = False  # Enable preview
