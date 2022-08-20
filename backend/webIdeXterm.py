#!/usr/bin/env python3
from flask import Flask, request
from flask_socketio import SocketIO
import pty
import os
import signal
import subprocess
import select
import termios
import struct
import fcntl
import psutil
import argparse

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["cmd"] = 'bash'
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins='*')

subprograms = {}


def set_winsize(fd, row, col, xpix=0, ypix=0):
    winsize = struct.pack("HHHH", row, col, xpix, ypix)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


def read_and_forward(sid):
    while True:
        socketio.sleep(0.01)
        if subprograms[sid]["fd"]:
            readable, _, _ = select.select([subprograms[sid]["fd"]], [], [], 0)
            if readable:
                output = os.read(subprograms[sid]["fd"], 1024 * 20).decode()
                socketio.emit("pty-output", {"output": output}, namespace="/pty", to=sid)
        else:
            del subprograms[sid]
            break


@socketio.on("pty-input", namespace="/pty")
def pty_input(data):
    if subprograms[request.sid]["fd"]:
        os.write(subprograms[request.sid]["fd"], data["input"].encode())


@socketio.on("resize", namespace="/pty")
def resize(data):
    if subprograms[request.sid]["fd"]:
        set_winsize(subprograms[request.sid]["fd"], data["rows"], data["cols"])


@socketio.on("connect", namespace="/pty")
def connect():
    print("==========connect")
    sid = request.sid
    print(sid)
    if sid in subprograms:
        return
    else:
        subprograms[sid] = {"fd": None, "child_pid": None}

    (child_pid, fd) = pty.fork()
    if child_pid == 0:
        subprocess.run(app.config["cmd"])
    else:
        subprograms[sid]["fd"] = fd
        subprograms[sid]["child_pid"] = child_pid
        set_winsize(fd, 50, 500)
        socketio.start_background_task(read_and_forward, sid)


@socketio.on("disconnect", namespace="/pty")
def disconnect():
    print("==========disconnect")
    sid = request.sid
    print(sid)
    os.close(subprograms[sid]["fd"])
    subprograms[sid]["fd"] = None
    os.kill(subprograms[sid]["child_pid"], signal.SIGKILL)
    p = psutil.Process(subprograms[sid]["child_pid"])
    for child in p.children(recursive=True):
        child.kill()
    p.wait()




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',required=True, type=int, default=5002)
    args = parser.parse_args()
    port=5002
    print(11)
    if args.port:
        port=args.port
        print(port)
    socketio.run(app, host='127.0.0.1', port=port)
