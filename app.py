from flask import Flask
from rcon import MCRcon
import argparse
import re

from threading import Thread
import traceback
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

def clock_thread(host,port,password):
    global resp
    print(type(port))
    port = int("25575")
    print(type(port))
    print("clock thread start")
    while True:
        print("clock exec")
        lock.acquire()
        print("locked")
        print("inloop:",type(port))
        try:
            with MCRcon(host,password,port) as mcr:
                print("connection open")
                res = mcr.command("/list")
                print("online")
                resp.online = True
                numbers = re.findall("\d+",res)
                resp.player_num = numbers[0]
                print(f"player_num:{numbers[0]}")
        except Exception:
            print(traceback.print_exc())
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
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    with open("config.json","r") as f:
        config = f.read()
    cfile = json.loads(config)
    host = cfile["host"]
    port = cfile["port"]
    if type(port)!=type(1):
        port = int(port)
    password = cfile["password"]
    print(f"host:{host},port:{port},password:{password}")

    web = Thread(target=lambda:app.run(host="0.0.0.0",port="3000"))
    #app.run(host="0.0.0.0",port="3000")
    clock=Thread(target=lambda:clock_thread(host=host,port=port,password=password))
    web.start()
    clock.start()

