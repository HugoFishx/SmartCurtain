
#!/usr/bin/env python
# -*- coding=utf-8 -*-
import socket
import threading
import time
import sys
import os
import struct
from time import sleep
import detect_image

def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('192.168.50.248', 12345))#这里换上自己的ip和端口
        # s.bind(('localhost', 12346))#这里换上自己的ip和端口
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print ("Waiting...")

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()

def deal_data(conn, addr):
    print ('Accept new connection from {0}'.format(addr))
    while 1:
        fileinfo_size = struct.calcsize('128sq')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sq', buf)
            fn = filename.strip(str.encode('\00'))
            new_filename = os.path.join(str.encode('./'), str.encode('new_') + fn)
            #print ('file new name is {0}, filesize if {1}'.format(new_filename, filesize))

            recvd_size = 0  # 定义已接收文件的大小
            fp = open('pic.jpg', 'wb')
            print ("start receiving...")
            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print("end receive...")
        print('start interferencing')
        try:
            detected =  detect_image.detect_func()
        except OSError:
            detected = 0
        if detected:
            conn.send(b'1')
            result='Detected!'
        else: 
            conn.send(b'0')
            result='Not Detected!'
        print('result sent:'+result)

        conn.close()
        break

if __name__ == '__main__':
    print('Edge TPU starts')
    socket_service()

    # python3 detect_image.py   --model test_data/ssd_mobilenet_v2_coco_quant_postprocess.tflite   --labels test_data/coco_labels.txt   --input test_data/grace_hopper.bmp   --output ${HOME}/grace_hopper_processed.bmp
