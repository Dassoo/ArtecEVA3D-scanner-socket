import socket
import subprocess
import os
import threading
import keyboard
import json
from cloud_upload import sweethive_upload

# Define server IP and port to listen on
hostname = socket.gethostname()
server_ip = socket.gethostbyname(hostname)
port = 3000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', port))

# Listen for incoming connections
sock.listen(1)

print(f"Server listening at {server_ip} on port {port}...")

def handle_command(conn, addr, command):
    print(f"Received command: {command}")

    if command == 'DOWNLOAD_REQUEST':  # Handle the download request
        try:
            # Split the command to get the file name
            filename = conn.recv(1024).decode()
            if os.path.exists(filename):
                conn.sendall(b'FILE_EXISTS')
                print(f"Sending file: {filename}")

                # Open the file for reading
                with open(filename, 'rb') as f:
                    # Send the file to the client
                    conn.sendall(f.read())
                    print(f"File sent: {filename}")
            else:
                conn.sendall(b'FILE_NOT_FOUND')
                print(f"File not found: {filename}")
        except Exception as e:
            print(f"Error downloading the requested file: {e}")
    elif command == 'PRESS_P':  # Handle the scanner pause request
        try:
            keyboard.press_and_release('p')  # Pressing the p key (pause scan)
            print("Pressed p key.")
        except Exception as e:
            print(f"Error pressing p key: {e}")
    elif command == 'PRESS_Q':  # Handle the scanner stop request
        try:
            keyboard.press_and_release('q')  # Pressing the q key (stop scan)
            print("Pressed q key.")
        except Exception as e:
            print(f"Error pressing q key: {e}")
    elif command == 'REQ':  # Handle the cloud upload
        try:
            # Receive additional data after the command
            data = conn.recv(1024).decode()
            folder, path, headers_json = data.split(',', 2)  # Split into folder, path, and headers
            headers = json.loads(headers_json)  # Deserialize headers
            print(f"Received cloud request with folder: {folder}, path: {path}, headers: {headers}")

            # Requesting upload to the dedicated software
            sweethive_upload(folder, path, headers)

        except Exception as e:
            print(f"Error processing cloud request: {e}")
    else:
        try:
            # Execute the command using subprocess
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            conn.sendall(output)
            conn.sendall(error)
        except Exception as e:
            print(f"Error executing command: {e}")

    conn.close()

while True:
    # Accept an incoming connection
    conn, addr = sock.accept()
    print(f"Connected by {addr}")

    # Receive the command from the client
    command = conn.recv(1024).decode()

    # Handle the command in a separate thread
    thread = threading.Thread(target=handle_command, args=(conn, addr, command))
    thread.start()
