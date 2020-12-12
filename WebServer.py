#! /usr/bin/python
# encoding:utf-8

# 导入Tornado模块
import tornado.ioloop
import tornado.httpserver
import tornado.web
import tornado.options
import RPi.GPIO as GPIO
import serial    #import serial module
ser = serial.Serial('/dev/ttyACM0', 9600,timeout=1)   #open named port at 9600,1s timeot

from tornado.options import define, options

define("port", type=int, default=12345, help="run on the given port")

def curtain_close():
    global ser
    ser.write('a')#writ a string to port
    return 0

def curtain_open():
    global ser
    ser.write('b')#writ a string to port
    return 0

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        status = 'Choose your operation'
        self.render('index.html', status=status)

class CurtainOpenHandler(tornado.web.RequestHandler):
    def get(self):
        curtain_open()
        status = 'Curtain has been opened!'
        self.render('index.html', status=status)

class CurtainCloseHandler(tornado.web.RequestHandler):
    def get(self):
        curtain_close()
        status = 'Curtain is now closed!'
        self.render('index.html', status=status)

class ImageHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-cache")

# urls = [(r"/", IndexHandler),(r"/open", CurtainOpenHandler),(r"/close", CurtainCloseHandler),(r"/(pic.png)", tornado.web.StaticFileHandler, {'path':'./'})]
settings = {"debug": True,}
urls = [(r"/", IndexHandler),(r"/open", CurtainOpenHandler),(r"/close", CurtainCloseHandler),(r"/(cap.jpeg)", ImageHandler, {'path':'./'}),]

def web_server():
    tornado.options.parse_command_line()
    app = tornado.web.Application(urls, **settings)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    web_server()

