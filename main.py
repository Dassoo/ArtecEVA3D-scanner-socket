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
from utils.viewer import open_viewer
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

# Function to run the scan in a separate thread
def run_scan():
    print("\n-- Scanning --")
    print("Starting in a few seconds...")
    start_scan(server_ip, port, path, folder)

# Main execution
if __name__ == '__main__':
    print(f"\n******* Project name: {folder} *******\n")

    print("Checking availability...")
    if is_port_open(server_ip, port):
        print(f"Port {port} is listening on {server_ip}")
    else:
        print(f"Port {port} on {server_ip} is not available")
        sys.exit(1)

    '''## stuff for continuous scanning
    # Start scanning in a separate thread
    scan_thread = threading.Thread(target=run_scan)
    scan_thread.start()

    # Allow for sending commands while scanning is ongoing
    ## Just a scanning example for testing out
    try:
        time.sleep(2)
        for i in range(10):
            pause_toggle(server_ip, port)
            time.sleep(2)
        stop_scan(server_ip, port)
    except KeyboardInterrupt:
        print("Interrupted! Stopping scan...")
        stop_scan(server_ip, port)

    # Wait for the scanning thread to finish before proceeding
    scan_thread.join()
    '''

    for i in range(10):
        status = start_scan(server_ip, port, path, folder)
        time.sleep(2)

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

    '''
    print("\nOpening the viewer...")
    print("(Press 'q' to quit the viewer, use 'o' and 'p' to navigate the frames)")
    open_viewer(path_to_current_project)
    '''
