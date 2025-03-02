import sys
import socket
import json

sys.path.append('.')

# OPEN AERARIUM SOFTWARE BEFORE REQUESTING
# result = subprocess.run(["C:/Users/iit_c/AppData/Local/Programs/Aerariumchain/Aerariumchain Desktop app.exe"], capture_output=True, text=True)
# time.sleep(10)

def cloud_request(server_ip, port, folder, path, headers):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((server_ip, port))

        message = f"{folder},{path},{json.dumps(headers)}"

        sock.send(b'REQ')
        sock.sendall(message.encode())  # Send data as bytes
        sock.close()

        print("Cloud upload request sent successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
