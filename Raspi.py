#!/usr/bin/env python
# -*- coding=utf-8 -*-

import socket
import os
import sys
import struct
from picamera import PiCamera
from time import sleep
import threading
from multiprocessing import Process, Manager
from WebServer import web_server, curtain_close, curtain_open
import RPi.GPIO as GPIO
import serial
try:
    ser = serial.Serial('/dev/ttyACM1', 9600,timeout=1)   #open named port at 9600,1s timeot
except:
    ser = serial.Serial('/dev/ttyACM0', 9600,timeout=1)
def socket_client(camera):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        filepath = 'cap.jpeg'
        s.connect(('192.168.50.248',12345))
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    while 1:
        camera.capture('cap.jpeg')
        sleep(2)
        # filepath = '/Users/yushiqi/Documents/GitHub/SmartCurtain/file'
        if os.path.isfile(filepath):
            fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath).encode('utf-8')),os.stat(filepath).st_size)
            s.send(fhead)
            print ('client filepath: {0}'.format(filepath))
            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print ('{0} file send over...'.format(filepath))
                    break
                s.send(data)
        print('send completed, wating for result')
        if s.recv(1024) == b'1':
            print('BB here!')
            people_detected = 1
        else:
            print('BB not here!')
            people_detected = 0
        s.close()
        break
    return people_detected

def edge_tpu():
        camera = PiCamera()
        while 1:
            if socket_client(camera):
                curtain_close()

        # while 1:
            # socket_client(camera)
            # if socket_client(camera) and curtain.open:
            #     curtain.close()
            #     sleep(10)
            #     while socket_client(camera):
            #         print('still there')
            #     curtain.open()

            # if sunrise() and not curtain.open:
            #     curtain.open()

if __name__ == '__main__':
        # edge_tpu_thread = threading.Thread(target=edge_tpu)
        # server_thread = threading.Thread(target=web_server)
        # edge_tpu_thread.start()
        # server_thread.start()
    manager = Manager()
    curtain_dict = manager.dict()
    curtain_dict['open'] = 0
    curtain_dict['busy'] = 0
    edge_tpu_process = Process(target=edge_tpu)
    server_process = Process(target=web_server)
    edge_tpu_process.start()
    server_process.start()
    edge_tpu_process.join()
    server_process.join()

            
            
