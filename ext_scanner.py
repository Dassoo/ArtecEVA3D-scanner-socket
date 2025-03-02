"""This file serves only the purpose of giving a package of functions for the robot movements script"""

import os
import sys
import shutil
import tomlkit
import time
import threading

from utils.check import is_port_open
from utils.scan import start_scan
from utils.zip import zip_files, unzip
from utils.download import download
from utils.request import cloud_request
from utils.pause_toggle import pause_toggle
from utils.stop_scan import stop_scan

sys.path.append('.')

# Loading settings
with open('settings.toml', 'r') as f:
    settings = tomlkit.parse(f.read())

server_ip = settings['server']['ip']
port = settings['server']['port']
path = settings['paths']['base']
folder = settings['paths']['folder']
token = settings['data']['auth_token']
headers = {'Authorization': 'Bearer ' + token}


def run_scan():
    """Function to run the scan in a separate thread."""
    print("\n-- Scanning --")
    print("Starting in a few seconds...")
    start_scan(server_ip, port, path, folder)


def start_scanning():
    """Start the scanning process."""
    print(f"\n******* Project name: {folder} *******\n")

    print("Checking availability...")
    if is_port_open(server_ip, port):
        print(f"Port {port} is listening on {server_ip}")
    else:
        print(f"Port {port} on {server_ip} is not available")
        sys.exit(1)

    # Start scanning in a separate thread
    scan_thread = threading.Thread(target=run_scan)
    scan_thread.start()

    return scan_thread


def pause_unpause_scanning():
    """Toggle the pause in the scanning process."""
    try:
        pause_toggle(server_ip, port)
    except KeyboardInterrupt:
        print("Interrupted! Stopping scan...")
        stop_scan(server_ip, port)


def stop_scanning():
    """Stop the scanning process."""
    stop_scan(server_ip, port)


def finalize_process(scan_thread):
    """Proceed with final steps after scanning."""
    # Wait for the scanning thread to finish before proceeding
    scan_thread.join()

    print("Zipping files...")
    zip_files(server_ip, port, path, folder)

    print("Downloading....")
    download(server_ip, port, path, folder)

    unzip(folder)

    try:
        shutil.move(folder, "projects")
    except Exception as e:
        print(e)

    path_to_current_project = f"projects/{folder}"
    if os.path.exists(path_to_current_project):
        print(f"The downloaded files are in: {path_to_current_project}")
    else:
        print("Something went wrong.")

    print(f"\nUploading {folder} project on cloud...")
    cloud_request(server_ip, port, folder, path_to_current_project, headers)

    # Viewer to be eventually added, temporarily disabled/not included


# EXECUTION EXAMPLE
'''
if __name__ == '__main__':
    # Start the scanning process
    scan_thread = start_scanning()

    # Pause/unpause the scanning process as you wish
    pause_unpause_scanning()
    time.sleep(5)
    pause_unpause_scanning()

    # Stop the scanning process
    stop_scanning()

    # Finalize processing after scanning is done
    finalize_process(scan_thread)
'''
