import socket
import time
import sys

sys.path.append('.')


def start_scan(server_ip, port, path, folder):
    start_time = time.time()

    # Create a socket object and connect to the server
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, port))
        # print("Successfully connected!")
    except Exception as e:
        print(e)

    # Send the command to execute
    command = f'start {path}/socket_server/app/cpp/scanExec.exe {path}/projects/{folder} \r\n'
    sock.send(command.encode())
    print(f"Sending scanning command to {server_ip}:{port}")

    # Wait for the response from the server
    # Not closing the connection until stuff is going on
    response = b''
    while True:
        data = sock.recv(1024)
        if not data:
            break
        response += data

    status = response.decode()
    print(f'{status}')

    sock.close()

    end_time = time.time()
    time_taken = end_time - start_time
    time_taken = round(time_taken, 2)
    print(f"Time elapsed: {time_taken}s\n")

    return status
