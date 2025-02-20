import os
# list of clients (e.g. camera units)
client_list = ['pi@192.168.0.100']
client_password = 'whatever' # password for client
client_data_path = '/home/pi/Data/' # path to data on client
server_data_path = '/home/pi/Downloads/birdcam/Data/' # path where data should go on server
fetch_then_move = False # trigger move2ext.py straight after finishing with fetching (something is off with this, so leave it False and call it separately)
ext_paths = ['/mnt/chickenHDD1/Data/','/mnt/chickenHDD2/Data'] # list of external paths
ext_checks = ['/mnt/chickenHDD1/Data/hello.check','/mnt/chickenHDD2/Data/hello.check'] # list of files to check if the external drive is mounted