import socket
import time
import os
import sys

sys.path.append('.')


def download(server_ip, port, path, folder):
    start_time = time.time()

    # Create a socket object and connect to the server
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, port))
        # print("Successfully connected!")
    except Exception as e:
        print(e)

    # Send the command to execute
    sock.sendall(b'DOWNLOAD_REQUEST')
    filename = f'{path}/projects/{folder}/{folder}.zip'
    print(f'Requesting file from server: {filename}')
    sock.sendall(filename.encode())
    response = sock.recv(1024).decode()
    # If the file exists send its data until fully downloaded
    if response == 'FILE_EXISTS':
        with open(os.path.basename(filename), 'wb') as f:
            while True:
                data = sock.recv(1024)
                if not data:
                    break
                f.write(data)
        print(f'File downloaded: {os.path.basename(filename)}')
    else:
        print(f'File not found: {os.path.basename(filename)}')

    time.sleep(3)

    sock.close()

    end_time = time.time()
    time_taken = end_time - start_time
    time_taken = round(time_taken, 2)
    print(f"Time elapsed: {time_taken}s\n")
