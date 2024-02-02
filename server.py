import multiprocessing
import queue
import time
from socket import *
import os
import threading
import random
import subprocess
from workers_function import workers
from datetime import datetime
import numpy as np


IP = "127.0.0.1"
PORT = 6000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = 'utf-8'

Path_queue = queue.Queue()
lock = threading.Lock()
error_count = np.zeros((5, 1))


jobl = threading.Lock()
jcc = threading.Lock()
job1 = []
job2 = []
job3 = []
job4 = []
job5 = []


def worker_creator(num, sock):
    while True:
        # worker_name = "worker %s" % num
        globals()["worker %s" % num] = multiprocessing.Process(target=workers, args=(num.__str__()))
        globals()["worker %s" % num].start()
        lock.acquire()
        loga = open("server.log", "a+")
        logw = datetime.now().time().__str__() + " - "
        loga.write(logw + "worker " + num + " started\n")
        loga.close()
        lock.release()
        print("worker " + num + " started")

        globals()["worker %s" % num].join()
        print("worker " + num + " died")


def workers_thread(conn, addr, num):
    while True:
        path = Path_queue.get()
        if num.__eq__("1"):
            job1.append(path)
        elif num.__eq__("2"):
            job2.append(path)
        elif num.__eq__("3"):
            job3.append(path)
        elif num.__eq__("4"):
            job4.append(path)
        elif num.__eq__("5"):
            job5.append(path)
        a = path.split("\\")
        lock.acquire()
        loga = open("server.log", "a+")
        logw = datetime.now().time().__str__() + " - "
        loga.write(logw + "request for creating " + a[len(a) - 1] + ".md5 was received\n")
        loga.close()
        lock.release()
        # print(logw+ "request for creating " + a[len(a)-1] + ".md5 was received")
        try:
            conn.send(path.encode(FORMAT))
        except:
            Path_queue.put(path)
            if num.__eq__("1"):
                job1.remove(path)
            elif num.__eq__("2"):
                job2.remove(path)
            elif num.__eq__("3"):
                job3.remove(path)
            elif num.__eq__("4"):
                job4.remove(path)
            elif num.__eq__("5"):
                job5.remove(path)
            return
        try:
            conn.recv(SIZE)
        except:
            # print("connection closed")
            return
    return


def commanders_thread(conn, code, path):
    a = path.split("\\")
    lock.acquire()
    loga = open("server.log", "a+")
    logw = datetime.now().time().__str__() + " - "
    loga.write(logw + "report for file " + a[len(a) - 1] + ".md5 was received\n")
    loga.close()
    lock.release()
    if code.__eq__("0"):
        Path_queue.put(path)
        #print("added")
        # print(path + " added")
    elif code.__eq__("1"):
        ndic = 0
        pro = 0
        for i in range(len(job1)):
            x = job1[i]
            if x.__eq__(path):
                ndic = 1
                pro = 1
                job1.remove(x)
                break
        if pro == 0:
            for i in range(len(job2)):
                x = job2[i]
                if x.__eq__(path):
                    ndic = 2
                    pro = 1
                    job2.remove(x)
                    break
        if pro == 0:
            for i in range(len(job3)):
                x = job3[i]
                if x.__eq__(path):
                    ndic = 3
                    pro = 1
                    job3.remove(x)
                    break
        if pro == 0:
            for i in range(len(job4)):
                x = job4[i]
                if x.__eq__(path):
                    ndic = 4
                    pro = 1
                    job4.remove(x)
                    break
        if pro == 0:
            for i in range(len(job5)):
                x = job5[i]
                if x.__eq__(path):
                    ndic = 5
                    pro = 1
                    job5.remove(x)
                    break
        if ndic == 0:
            Path_queue.put(path)
        else:
            #print(ndic)
            error_count[ndic - 1] = error_count[ndic - 1] + 1
            if error_count[ndic - 1] == 2:
                # globals()["worker %s" % ndic].kill()
                error_count[ndic - 1] = 0
                lock.acquire()
                logct = open("server.log", "a+")
                logwct = datetime.now().time().__str__() + " - "
                logct.write(logwct + "worker " + ndic.__str__() + " killed!\n")
                logct.close()
                lock.release()
                print("worker " + ndic.__str__() + "killed")
            Path_queue.put(path)
        #print("done")
    conn.send("accepted".encode(FORMAT))

    while True:
        one = conn.recv(SIZE).decode(FORMAT)
        two = one.split(" ")
        #print(one)
        if two[1].__eq__("0"):
            Path_queue.put(two[2])
            #print("added")
            # print(two[2] + " added")
        elif two[1].__eq__("1"):
            Path_queue.put(two[2])
            ndic = 0
            pro = 0
            #jcc.acquire()
            for i in range(len(job1)):  # w1
                x = job1[i]
                if x.__eq__(two[2]):
                    ndic = 1
                    pro = 1
                    job1.remove(two[2])
                    break
            if pro == 0:  # w2
                for i in range(len(job2)):
                    x = job2[i]
                    if x.__eq__(two[2]):
                        ndic = 2
                        pro = 1
                        job2.remove(two[2])
                        break
            if pro == 0:
                for i in range(len(job3)):
                    x = job3[i]
                    if x.__eq__(two[2]):
                        ndic = 3
                        pro = 1
                        job3.remove(two[2])
                        break
            if pro == 0:
                for i in range(len(job4)):
                    x = job4[i]
                    if x.__eq__(path):
                        ndic = 4
                        pro = 1
                        job4.remove(two[2])
                        break
            if pro == 0:
                for i in range(len(job5)):
                    x = job5[i]
                    if x.__eq__(two[2]):
                        ndic = 5
                        pro = 1
                        job5.remove(two[2])
                        break
            #jcc.release()
            if ndic == 0:
                #print("thief not found!")
                conn.send("accepted".encode(FORMAT))
                continue
            else:
                jobl.acquire()
                #print(ndic)
                error_count[ndic - 1] = error_count[ndic - 1] + 1
                #print(error_count[ndic - 1])
                if error_count[ndic - 1] >= 2:
                    globals()["worker %s" % ndic].kill()
                    error_count[ndic - 1] = 0
                    lock.acquire()
                    logct = open("server.log", "a+")
                    logwct = datetime.now().time().__str__() + " - "
                    logct.write(logwct + "worker " + ndic.__str__() + " killed!\n")
                    logct.close()
                    lock.release()
                    print("worker " + ndic.__str__() + " killed")
                jobl.release()
                #Path_queue.put(two[2])
            #print("done")
        conn.send("accepted".encode(FORMAT))

    return


def start(s):
    s.listen()
    for i in range(5):
        z = i + 1
        thread = threading.Thread(target=worker_creator, args=(z.__str__(), s))
        thread.start()

    while True:
        # print("main")
        addr, L = s.accept()
        x = addr.recv(SIZE).decode(FORMAT)
        req = x.split(" ")
        if req[0].__eq__("worker"):
            thread1 = threading.Thread(target=workers_thread, args=(addr, L, req[1]))
            thread1.start()
        elif req[0].__eq__("commander"):
            thread2 = threading.Thread(target=commanders_thread, args=(addr, req[1], req[2]))
            thread2.start()


if __name__ == "__main__":
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(ADDR)
    print("[STARTING] server is listening to you(dont fear tho) ....")
    log = datetime.now().time().__str__() + " - "
    log = log + "[STARTING] server is listening to you(dont fear tho) ....\n"
    logs = open("server.log", "a+")
    logs.write(log)
    logs.close()
    start(s)
