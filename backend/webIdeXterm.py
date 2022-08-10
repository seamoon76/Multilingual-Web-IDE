#!/usr/bin/env python3
import argparse
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import pty
import os
import signal
import subprocess
import select
import termios
import struct
import fcntl



app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["cmd"] = 'bash'
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins='*')

subprograms = {}

def set_winsize(fd, row, col, xpix=0, ypix=0):
    winsize = struct.pack("HHHH", row, col, xpix, ypix)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


def read_and_forward_pty_output(sid):
    max_read_bytes = 1024 * 20
    while True:
        socketio.sleep(0.01)
        if subprograms[sid]["fd"]:
            timeout_sec = 0
            (data_ready, _, _) = select.select([subprograms[sid]["fd"]], [], [], timeout_sec)
            if data_ready:
                output = os.read(subprograms[sid]["fd"], max_read_bytes).decode(encoding='UTF-8')
                socketio.emit("pty-output", {"output": output}, namespace="/pty", to=sid)
        else:
            del subprograms[sid]
            break


@app.route('/')
def index():
    return None


@socketio.on("pty-input", namespace="/pty")
def pty_input(data):
    sid = request.sid
    print(sid)
    if subprograms[sid]["fd"]:
        os.write(subprograms[sid]["fd"], data["input"].encode(encoding='UTF-8'))


@socketio.on("resize", namespace="/pty")
def resize(data):
    sid = request.sid
    print(sid)
    if app.config["fd"]:
        set_winsize(subprograms[sid]["fd"], data["rows"], data["cols"])


@socketio.on("connect", namespace="/pty")
def connect():
    sid = request.sid
    print(sid)
    if sid in subprograms:
        # already started child process, don't start another
        return
    else:
        subprograms[sid] = {"fd": None, "child_pid": None}

    # create child process attached to a pty we can read from and write to
    (child_pid, fd) = pty.fork()
    if child_pid == 0:
        # this is the child process fork.
        # anything printed here will show up in the pty, including the output
        # of this subprocess
        subprocess.run(app.config["cmd"])
    else:
        # this is the parent process fork.
        # store child fd and pid
        subprograms[sid]["fd"] = fd
        subprograms[sid]["child_pid"] = child_pid
        set_winsize(fd, 50, 500)
        socketio.start_background_task(read_and_forward_pty_output, sid)

@socketio.on("disconnect", namespace="/pty")
def disconnect():
    print("==========disconnect")
    sid = request.sid
    print(sid)
    os.kill(subprograms[sid]["child_pid"], signal.SIGKILL)
    subprograms[sid]["fd"] = None

if __name__ == "__main__":
    socketio.run(app, host='127.0.0.1',port=5002)
