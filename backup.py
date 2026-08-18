"""
Backup Program
Author: Dylan Breeze
Email: your-email@example.com
Version: 1.0

Description:
    Performs full backups of files and directories.

Usage:
    python backup.py <job_name>
"""
import os
import sys
import pathlib
import shutil
from datetime import datetime
import backupcfg

def main():
    jobName = sys.argv[1]
    try:
        SourcePath = backupcfg.backup_jobs[jobName]["source"]
        DestinationPath = backupcfg.backup_jobs[jobName]["destination"]
    except:
        print(f"ERROR: Job '{jobName}' not found in backup configuration.")
    if CheckPathExists(SourcePath) and CheckPathExists(DestinationPath):
        CopyFiles(SourcePath, DestinationPath)

def CheckPathExists(path):
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

def CopyFiles(srcPath, dstPath):
    try:
        dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        srcPath = pathlib.Path(srcPath)
        dstPath = pathlib.Path(dstPath)

        # If it's a file, keep the extension at the end
        if srcPath.is_file():
            newName = srcPath.stem + "-" + dateTimeStamp + srcPath.suffix
            shutil.copy2(srcPath, dstPath / newName)

        # If it's a folder, copy the whole folder to a new folder name
        elif srcPath.is_dir():
            newFolderName = srcPath.name + "-" + dateTimeStamp
            shutil.copytree(srcPath, dstPath / newFolderName)

    except:
        print("An error occurred while copying files.")

if __name__ == "__main__":
    main()