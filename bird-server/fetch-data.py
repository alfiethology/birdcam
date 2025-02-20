#!/usr/bin/env python3

import os
import subprocess
from fetch_settings import *

def main():
	# check if rsync is already running, otherwise create a lock
	if os.path.exists("/tmp/rsyncjob.lock"):
		print("Rsync is already in progress... exiting")
	else:
		# create lock
		os.system("touch /tmp/rsyncjob.lock")
		try:
			# try to fetch data from each raspberry
			for ii in range(len(client_list)):
				# create folder on the server (if it does not exist)
				#client_name = client_list[ii].split(".")[0]
				#server_path_data = os.path.join(server_data_path,client_name)
				# pull data over
				#if not os.path.exists(server_path_data):
				#	os.makedirs(server_path_data)
				command_data = "sshpass -p \""+client_password+"\" rsync -rvz --exclude=\'*.h264\' --remove-source-files --prune-empty-dirs -e \'ssh -o StrictHostKeyChecking=no -p 22\' --progress "+client_list[ii]+":"+client_data_path+"/ "+server_data_path+'/'
				try:
					subprocess.call(command_data, shell=True)
				except:
					print("error with data")
			# delete lock
			os.system("rm /tmp/rsyncjob.lock")
		except:
			# delete lock
			os.system("rm /tmp/rsyncjob.lock")
		if fetch_then_move:
			os.system('/home/pi/animal-monitor-server/move2ext.py')

if __name__ == '__main__':
	main()
