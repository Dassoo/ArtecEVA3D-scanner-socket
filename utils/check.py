import socket
import sys

sys.path.append('.')


def is_port_open(server_ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)  # Set a timeout to avoid blocking indefinitely
    try:
        s.connect((server_ip, port))
        s.close()
        return True
    except:
        return False
