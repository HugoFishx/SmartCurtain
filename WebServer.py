#! /usr/bin/python
# encoding:utf-8

# 导入Tornado模块
import tornado.ioloop
import tornado.httpserver
import tornado.web
import tornado.options
import RPi.GPIO as GPIO

from tornado.options import define, options

define("port", type=int, default=12345, help="run on the given port")

def curtain_close():
    return 0

def curtain_open():
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

def web_server(curtain_dict):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    tornado.options.parse_command_line()
    app = tornado.web.Application(urls, **settings)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    # web_server()
    pass