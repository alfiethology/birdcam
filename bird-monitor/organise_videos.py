import os
import shutil
import re

def reorganize_videos(input_dir, output_dir):
    """
    Reorganize videos from:
    ./Data/raw_videos/{camera_name}_{YYYY_MM_DD}/{camera_name}_cam0_{YYYY_MM_DD}-{HH_MM_SS}.mp4
    To:
    ./Data/reorganised_videos/YYYY-MM-DD/camera_name/HH_MM_SS.mp4

    Args:
        input_dir (str): Path to the directory containing raw videos.
        output_dir (str): Path to the output directory for organized videos.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Walk through each camera_date folder in the input directory
    for folder in os.listdir(input_dir):
        folder_path = os.path.join(input_dir, folder)

        if not os.path.isdir(folder_path):
            continue  # Skip non-directory items

        # Extract camera_name and date using regex
        match = re.match(r"(.+?)_(\d{4}_\d{2}_\d{2})$", folder)
        if not match:
            print(f"Skipping folder {folder} (unexpected format)")
            continue

        camera_name, raw_date = match.groups()
        date = raw_date.replace("_", "-")  # Convert YYYY_MM_DD to YYYY-MM-DD

        # Correct folder paths
        date_folder = os.path.join(output_dir, date)
        camera_folder = os.path.join(date_folder, camera_name)

        # Create necessary folders
        os.makedirs(camera_folder, exist_ok=True)

        # Process each video file in the folder
        for video_file in os.listdir(folder_path):
            if not video_file.endswith(".mp4"):
                continue  # Skip non-video files

            # Extract time from the filename: camera_name_cam0_{YYYY_MM_DD}-{HH_MM_SS}.mp4
            match = re.search(r"-(\d{2}_\d{2}_\d{2})\.mp4$", video_file)
            if not match:
                print(f"Skipping file {video_file} (unexpected format)")
                continue  # Skip files that don't match expected format

            time = match.group(1)  # Extract HH_MM_SS
            new_filename = f"{time}.mp4"

            # Move the video file to the correct folder
            source_path = os.path.join(folder_path, video_file)
            destination_path = os.path.join(camera_folder, new_filename)

            shutil.move(source_path, destination_path)
            print(f"Moved {source_path} -> {destination_path}")

        # Remove the original folder if it's now empty
        if not os.listdir(folder_path):
            os.rmdir(folder_path)
            print(f"Deleted empty folder: {folder_path}")

    # Now remove any zero-byte files in the output directory
    remove_zero_byte_files(output_dir)

    print("Reorganization complete!")

def remove_zero_byte_files(directory):
    """
    Recursively removes any zero-byte MP4 files from the given directory.

    Args:
        directory (str): Path to the directory to scan for zero-byte files.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp4"):
                file_path = os.path.join(root, file)
                if os.path.getsize(file_path) == 0:
                    os.remove(file_path)
                    print(f"Deleted zero-byte file: {file_path}")

    print("Reorganization complete!")

if __name__ == "__main__":
    input_directory = "/media/or22503/ChickenHDD5/Data/raw_videos/"
    output_directory = "/media/or22503/ChickenHDD5/Data/reorganised_videos/"
    reorganize_videos(input_directory, output_directory)
