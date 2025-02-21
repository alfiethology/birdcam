import subprocess

# Define the scripts to run in order
scripts = [
    "/home/pi/birdcam/bird-server/fetch-data.py",
    "/home/pi/birdcam/bird-server/organise-videos.py",
    "/home/pi/birdcam/bird-server/move2ext.py"
]

for script in scripts:
    try:
        print(f"Running {script}...")
        subprocess.run(["python3", script], check=True)
        print(f"{script} completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script}: {e}\n")
        break  # Stop execution if any script fails

print("Pipeline execution finished.")
