from flask import Flask
from rcon import MCRcon

from threading import Thread
import time
import threading
import json

lock = threading.Lock()

app = Flask(__name__)
class status:
    def __init__(self):
        self.online:bool = False
        self.player_num = 0

resp = status()

def clock_thread():
    global resp
    print("clock thread start")
    while True:
        print("clock exec")
        lock.acquire()
        print("locked")
        try:
            with MCRcon("localhost", "111111q.", 25575) as mcr:
                print("connection open")
                res = mcr.command("/list")
                print("online")
                resp.online = True
        except Exception:
            resp.online = False
            print("offline")
        lock.release()
        print("lock released")
        time.sleep(10)


@app.route("/api/status")
def hello_world():
    global resp
    res = {
        "status":resp.online,
        "player_num":resp.player_num,
    }
    # return "online" if resp.online else "offline"
    print(res)
    return res


if __name__== '__main__':
    web = Thread(target=lambda:app.run(host="0.0.0.0",port="3000"))
    #app.run(host="0.0.0.0",port="3000")
    clock=Thread(target=clock_thread)
    web.start()
    clock.start()

