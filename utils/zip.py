import socket
import sys
import time
import os
import zipfile

sys.path.append('.')


def zip_files(server_ip, port, path, folder):
    start_time = time.time()

    # Create a socket object and connect to the server
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, port))
        # print("Successfully connected!")
    except Exception as e:
        print(e)

    # Send the command to execute
    command = f'cd {path}/projects/{folder} && tar -a -c -f {folder}.zip *.png *.mtl *.obj\r\n'
    sock.send(command.encode())
    print(f"Sending zipping command to {server_ip}:{port}")

    # Wait for the response from the server
    # Not closing the connection until stuff is going on
    response = b''
    while True:
        data = sock.recv(1024)
        if not data:
            break
        response += data

    sock.close()

    end_time = time.time()
    time_taken = end_time - start_time
    time_taken = round(time_taken, 2)
    print(f"Time elapsed: {time_taken}s\n")


# Unzip the frames folder downloaded from the server
def unzip(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    with zipfile.ZipFile(f'{folder}.zip', 'r') as zip_ref:
        zip_ref.extractall(folder)
        zip_ref.close()

    os.remove(f'{folder}.zip')
