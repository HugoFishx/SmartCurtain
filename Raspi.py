#!/usr/bin/env python
# -*- coding=utf-8 -*-

import socket
import os
import sys
import struct
from picamera import PiCamera
from time import sleep

def socket_client(camera):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        filepath = '/home/pi/Desktop/cap.jpg'
        s.connect(('192.168.50.248',12345))
# s.connect(('localhost',12346))
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
        else:
            print('BB not here!')
        s.close()
        break

if __name__ == '__main__':
        camera = PiCamera()
        while 1:
            socket_client(camera)
