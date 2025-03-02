import socket
import sys

sys.path.append('.')

def pause_toggle(server_ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, port))

    sock.send(b'PRESS_P')
    sock.close()
