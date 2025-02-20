#!/usr/bin/env python3
import os
import subprocess
from fetch_settings import *

def main():
	# check if rsync is already running, otherwise create a lock
	if os.path.exists("/tmp/rsyncjob_move2ext.lock"):
		print("Rsync is already in progress... exiting")
	else:
		# create lock
		os.system("touch /tmp/rsyncjob_move2ext.lock")
		for ii in range(len(ext_paths)):
			if os.path.exists(ext_checks[ii]):
				# rsync command to run
				command_move2ext = "rsync -rvz --exclude=\'*.tmp\' --remove-source-files "+server_data_path+"/* "+ext_paths[ii]+'/'
				try:
					# call command
					subprocess.call(command_move2ext, shell=True)
				except:
					print("Error with moving data to external location")
			else:
				print(ext_paths[ii]+": External path does not exist... moving on to the next one")
		# delete lock
		os.system("rm /tmp/rsyncjob_move2ext.lock")

if __name__ == '__main__':
	main()
