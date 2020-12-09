import socket
import time
host = '192.168.50.219'  # IP of edge tpu
# host = 'localhost'
port = 8083
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
client.connect((host, port))
while True:
    client.send(time.asctime(time.localtime(time.time())).encode())
    print('send data')
    time.sleep(10)
