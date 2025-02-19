import os

var_resolution = (1644, 1232)  # Camera resolution
var_framerate = 30  # Framerate
var_vflip = True  # Vertical flip
var_length = 10  # Recording length in seconds (Updated for NIR sensor)
var_pir = True  # Enable motion sensor trigger (set to True)
var_pir_gpio = 17  # GPIO pin for NIR motion sensor
var_out_folder = '/home/pi/Data/'  # Output folder
var_preview = False  # Enable preview
var_record_external = False  # Record to external storage
var_external_paths = ('/mnt/Feeder01/Data/', '/mnt/Feeder02/Data/')  # External storage paths
var_usb_device = '/dev/video1'  # USB camera device location
