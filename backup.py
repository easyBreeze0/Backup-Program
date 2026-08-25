"""
Backup Program
Author: Dylan Breeze
Email: dylan.breeze@outlook.com
Version: 1.6.1

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
import smtplib

import backupcfg


def check_path_exists(path, job_name="unknown"):
    """Check whether the specified path exists."""

    try:
        # Check whether the provided path exists.
        if os.path.exists(path):
            print(f"Path {path} exists.")
            return True
        else:
            error_message = f"Path {path} does not exist."
            report_error(job_name, error_message)
        return False

    # Handle errors that occur while checking the path.
    except Exception:
        error_message = "An error occurred while checking the path existence."
        report_error(job_name, error_message)
        return False


def copy_files(source_path, destination_path, job_name="unknown"):
    """Copy the specified file or directory to the destination."""

    try:
        # Generate a timestamp so that each backup can have a unique name.
        date_time_stamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        source_path = pathlib.Path(source_path)
        destination_path = pathlib.Path(destination_path)

        # If the source is a file, create a timestamped copy while
        # keeping the original file extension.
        if source_path.is_file():
            new_name = (
                source_path.stem
                + "-"
                + date_time_stamp
                + source_path.suffix
            )
            shutil.copy2(source_path, destination_path / new_name)

        # If the source is a directory, copy the entire directory
        # to a new timestamped directory.
        elif source_path.is_dir():
            new_folder_name = source_path.name + "-" + date_time_stamp
            shutil.copytree(
                source_path,
                destination_path / new_folder_name
            )

        success_message = "Backup completed successfully."
        print(success_message)
        write_log(job_name, "SUCCESS")
        send_email(f"Backup job '{job_name}' completed successfully.")

    # Handle errors that occur while copying the source.
    except Exception:
        error_message = "An error occurred while copying files."
        report_error(job_name, error_message)


def report_error(job_name, error_message):
    """Print an error message and write it to the log."""

    # Print the error message to the console.
    print(f"ERROR: {error_message}")

    # Write the error to the log file and send an email notification.
    write_log(job_name, "FAIL", error_message)
    send_email(f"Backup job '{job_name}' failed with error: {error_message}")


def write_log(job_name, status, error_message=""):
    """Write a log entry for the backup job."""

    try:
        # Get the current date and time for the log entry.
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create the log entry string.
        log_entry = f"{current_time} - Job: {job_name} - Status: {status}"
        if error_message:
            log_entry += f" - Error: {error_message}"

        # Write the log entry to the log file.
        with open(backupcfg.log_file, "a") as log_file:
            log_file.write(log_entry + "\n")

    # Handle errors that occur while writing to the log file.
    except Exception as e:
        print(f"An error occurred while writing to the log file: {e}")


def send_email(message):
    """Send an email notification with the specified message."""

    # Store the email server and account details.
    smtp = {"sender":    "hexypup@gmail.com",
    "recipient": "30026674@students.sunitafe.edu.au",
    "server":    "smtp.elasticemail.com",
    "port":      2525,
    "user":      "hexypup@gmail.com",
    "password":  "D4CA465B984C46A44F44297574BAB4C2BF1A"}

    # Create the email message with the recipient, sender, subject, and body.
    email = 'To: ' + smtp["recipient"] + '\n' + 'From: ' + smtp["sender"] + '\n' + 'Subject: Backup Error\n\n' + message + '\n'
    
    try:
        # Connect to the email server and send the notification.
        with smtplib.SMTP(smtp["server"], smtp["port"], timeout=10) as smtp_server:
            smtp_server.ehlo()
            smtp_server.starttls()
            smtp_server.ehlo()
            smtp_server.login(smtp["user"], smtp["password"])
            smtp_server.sendmail(smtp["sender"], smtp["recipient"], email)
            print("Email notification sent successfully.")

    # Handle errors that occur while sending the email notification.
    except Exception as e:
        print(f"ERROR: Email notification failed: {e}")


def main():
    """Load the selected backup job and start the backup process."""

    # Check that at least one backup job was provided.
    if len(sys.argv) < 2:
        error_message = "No job name provided."
        report_error("unknown", error_message)
        return

    # Process each backup job provided on the command line.
    for job_name in sys.argv[1:]:
        # Get the source and destination paths for the selected backup job.
        try:
            source_path = backupcfg.backup_jobs[job_name]["source"]
            destination_path = backupcfg.backup_jobs[job_name]["destination"]
        except KeyError:
            error_message = f"Job '{job_name}' not found in backup configuration."
            report_error(job_name, error_message)
            continue

        # Check that both the source and destination paths exist before
        # attempting to perform the backup.
        if check_path_exists(source_path, job_name) and check_path_exists(
            destination_path, job_name
        ):
            copy_files(source_path, destination_path, job_name)
        else:
            error_message = "Source or destination path does not exist."
            report_error(job_name, error_message)

# Run the main function when the program is executed directly.
if __name__ == "__main__":
    main()