# coding=utf-8
import socket

BUF_SIZE = 1024
host = '192.168.50.219'  # IP of raspi
host = 'localhost'
port = 8083

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)
client, address = server.accept()
while True:
    data = client.recv(BUF_SIZE)
    print(data.decode())
    # client.close()
