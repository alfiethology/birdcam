import subprocess
import signal
import sys
import os
from fetch_settings import *

LOCK_FILE = "/tmp/rsyncjob.lock"

def cleanup_lock_file():
    """Remove the lock file on exit."""
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

def main():
    # Check if rsync is already running
    if os.path.exists(LOCK_FILE):
        print("Rsync is already in progress... exiting")
        sys.exit(0)
    
    # Create lock file with the current process ID
    with open(LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))

    # Ensure lock file is removed on script exit
    signal.signal(signal.SIGTERM, lambda signum, frame: cleanup_lock_file())
    signal.signal(signal.SIGINT, lambda signum, frame: cleanup_lock_file())

    try:
        for client in client_list:
            command_data = f"sshpass -p \"{client_password}\" rsync -rvz --exclude='*.h264' --remove-source-files --prune-empty-dirs -e 'ssh -o StrictHostKeyChecking=no -p 22' --progress {client}:{client_data_path}/ {server_data_path}/"
            
            print(f"Running command: {command_data}")
            result = subprocess.run(command_data, shell=True, capture_output=True, text=True)
            
            # Print rsync output
            print(f"STDOUT:\n{result.stdout}")
            print(f"STDERR:\n{result.stderr}")
            print(f"Rsync exited with code {result.returncode}")

            # Handle rsync errors
            if result.returncode not in [0, 24]:  # 24 means "some files vanished"
                print(f"Error: Rsync failed with exit code {result.returncode}")
                return result.returncode  # Exit with rsync's error code
        
        if fetch_then_move:
            move_command = "/home/pi/animal-monitor-server/move2ext.py"
            print(f"Running {move_command}...")
            move_result = subprocess.run(["python3", move_command], capture_output=True, text=True)
            
            # Print move2ext.py output
            print(f"Move script STDOUT:\n{move_result.stdout}")
            print(f"Move script STDERR:\n{move_result.stderr}")

            if move_result.returncode != 0:
                print(f"Error: Move script failed with exit code {move_result.returncode}")
                return move_result.returncode  # Exit with move script's error code
        
        return 0  # Success

    finally:
        cleanup_lock_file()  # Remove lock file

if __name__ == '__main__':
    exit_code = main()
    print(f"fetch-data.py completed with exit code {exit_code}")
    sys.exit(exit_code)  # Ensure the correct exit code is returned
