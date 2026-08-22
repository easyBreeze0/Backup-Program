"""
Backup Program
Author: Dylan Breeze
Email: dylan.breeze@outlook.com
Version: 1.3

Description:
    Performs full backups of files and directories.

Usage:
    python backup.py <job_name>
"""

import os
import pathlib
import shutil
import sys
from datetime import datetime

import backupcfg


def main():
    try:
        job_name = sys.argv[1]
    except:
            print("ERROR: when loading job name from command line arguments.")
            return
    try:
        source_path = backupcfg.backup_jobs[job_name]["source"]
        destination_path = backupcfg.backup_jobs[job_name]["destination"]
    except:
        print(f"ERROR: Job '{job_name}' not found in backup configuration.")
        return

    if check_path_exists(source_path) and check_path_exists(destination_path):
        copy_files(source_path, destination_path)

def check_path_exists(path):
    try:
        if os.path.exists(path):
            print(f"Path {path} exists.")
            return True
        else:
            print(f"Path {path} does not exist.")
        return False
    except:
        print("An error occurred while checking the path existence.")
        return False


def copy_files(source_path, destination_path):
    try:
        date_time_stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        source_path = pathlib.Path(source_path)
        destination_path = pathlib.Path(destination_path)

        # If it's a file, keep the extension at the end.
        if source_path.is_file():
            new_name = (
                source_path.stem
                + "-"
                + date_time_stamp
                + source_path.suffix
            )
            shutil.copy2(source_path, destination_path / new_name)

        # If it's a folder, copy the whole folder to a new folder name.
        elif source_path.is_dir():
            new_folder_name = source_path.name + "-" + date_time_stamp
            shutil.copytree(
                source_path,
                destination_path / new_folder_name
            )

    except:
        print("An error occurred while copying files.")


if __name__ == "__main__":
    main()