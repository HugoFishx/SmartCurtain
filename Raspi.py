#!/usr/bin/env python
# -*- coding=utf-8 -*-

import socket
import os
import sys
import struct
from picamera import PiCamera
from time import sleep
import threading
from WebServer import web_server

class Curtain:
    def __init__(self):
        self.open = 0

    def close(self):
        self.open = 0
        return 0

    def open(self):
        self.open = 1
        return 0

def socket_client(camera):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        filepath = '/home/pi/Desktop/cap.jpg'
        s.connect(('192.168.50.248',12345))
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    while 1:
        camera.capture('/home/pi/Desktop/cap.jpg')
        sleep(5)
        # filepath = '/Users/yushiqi/Documents/GitHub/SmartCurtain/file'
        if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            # 定义文件头信息，包含文件名和文件大小
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
        curtain = Curtain()
        while 1:
            if socket_client(camera) and curtain.open:
                curtain.close()
                sleep(10)
                while socket_client(camera):
                    print('still there')
                curtain.open()

            if sunrise() and not curtain.open:
                curtain.open()

def web_server():
    return 0

if __name__ == '__main__':
        edge_tpu_thread = threading.Thread(target=edge_tpu)
        server_thread = threading.Thread(target=web_server)
            
            
