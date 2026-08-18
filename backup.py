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

def main():
    SourcePath = r"C:\Test_Source\test.txtt"
    DestinationPath = r"C:\Test_Destination"
    CheckFileExists(SourcePath);

def CheckFileExists(file_path):
    try:
        if os.path.exists(file_path):
            print(f"File {file_path} does exist.")
            return True
        else:
            print(f"File {file_path} does not exist.")
        return False
    except:
        print("An error occurred while checking the file existence.")
        return False

if __name__ == "__main__":
    main()