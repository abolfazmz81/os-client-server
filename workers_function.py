import hashlib
from random import random
import time
from socket import *
from datetime import datetime

IP = "127.0.0.1"
PORT = 6000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = 'utf-8'


def workers(num):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(ADDR)
    ch = random()
    while True:
        # print("here")
        sock.send(("worker " + num + " send Path").encode(FORMAT))
        try:
            test = sock.recv(1024).decode(FORMAT)
        except:
            return
        testmd5 = test + ".md5"
        file = open(test, "r")
        fmd5 = open(testmd5, "a")
        lines = file.readlines()
        file.close()
        final = ''
        for x in range(0, len(lines)):
            final = final + lines[x]
        rand = random()
        if rand > ch:
            final = "bug"
        else:
            final = final

        md5w = hashlib.md5(final.encode()).hexdigest()
        fmd5.write(md5w)
        fmd5.close()
        # print("done")
        xa = test.split("\\")
        xa2 = testmd5.split("\\")
        log = datetime.now().time().__str__() + " - "
        log = log + xa[len(xa) - 1] + " was converted to " + xa2[len(xa2) - 1] + "\n"
        # print(log)
        logf = open("worker_log_" + num + ".log", "a+")
        logf.write(log)
        logf.close()
        time.sleep(0.1)
