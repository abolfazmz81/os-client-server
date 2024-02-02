from socket import *
import os
import threading
import re
import queue
import os
import glob
from datetime import datetime
import hashlib

IP = "127.0.0.1"
PORT = 6000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = 'utf-8'
lock = threading.Lock()
Path_queue = queue.Queue()
s = socket(AF_INET, SOCK_STREAM)
s.connect(ADDR)


def file_address_extractor(basepath):
    """
    A function to extract the addresses of the files located in basepath path
    """
    for i in glob.glob("TransactionFiles/subfolder/*.json"):
        text = i.split("\\")
        Path_queue.put("TransactionFiles/subfolder\\" + text[1])

    return


def authentication_commanders():
    while True:
        path = Path_queue.get()
        # print(path)
        # lock.acquire()
        try:
            file = open(path + ".md5", "r")
        except:
            lock.acquire()
            xa = path.split("\\")
            log = datetime.now().time().__str__() + " - "
            log = log + "file " + xa[len(xa) - 1] + " was not converted to .md5 \n"
            logc = open("commander.log", "a+")
            logc.write(log)
            logc.close()
            s.send(("commander 0 " + path).encode(FORMAT))
            s.recv(SIZE)
            lock.release()
            Path_queue.put(path)
            # print("path " + path + " puted back in")
        else:
            com = file.readlines()
            file.close()
            file1 = open(path, "r")
            lines = file1.readlines()
            file1.close()
            final = ''
            for x in range(0, len(lines)):
                final = final + lines[x]
            md5w = hashlib.md5(final.encode()).hexdigest()
            if md5w.__eq__(com[0]):
                # Path_queue.__delattr__(path)
                print("good file" + path)
            else:
                lock.acquire()
                #Path_queue.put(path)
                print("path " + path + " puted back in")
                s.send(("commander 1 " + path).encode(FORMAT))
                s.recv(SIZE)
                xa = path.split("\\")
                log = datetime.now().time().__str__() + " - "
                log = log + "file " + xa[len(xa) - 1] + " was incorrectly converted to .md5 \n"
                logc = open("commander.log", "a+")
                logc.write(log)
                logc.close()
                lock.release()
                # print("file" + path + " was correctly converted")
        # print("around here")
        # lock.release()

    return


if __name__ == "__main__":
    oogga = 0

    lock.acquire()
    log = datetime.now().time().__str__() + " - "
    log = log + "commander started working\n"
    logc = open("commander.log", "a+")
    logc.write(log)
    logc.close()
    lock.release()

    thread = threading.Thread(target=file_address_extractor("."))
    thread.start()
    thread.join()


    for zaza in range(5):
        thread1 = threading.Thread(target=authentication_commanders)
        thread1.start()
    while True:
        oogga = oogga + 1
