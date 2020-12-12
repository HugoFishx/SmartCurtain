#! /usr/bin/python
# encoding:utf-8

# 导入Tornado模块
import tornado.ioloop
import tornado.httpserver
import tornado.web
import tornado.options

from tornado.options import define, options

define("port", type=int, default=12345, help="run on the given port")

class Object():
    def __init__(self):
        self.busy = 0
        self.closed = 0

    def open(self):
        return 0
    def close(self):
        return 0

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        status = 'Choose your operation'
        if not curtain_dict['open']:
            curtain_status = 'closed'
        else:
            curtain_status = 'open'
        self.render('index.html', status=status, curtain_status=curtain_status)

class CurtainOpenHandler(tornado.web.RequestHandler):
    def get(self):
        while curtain_dict['busy']:
            pass
        curtain_open()
        status = 'Curtain has been opened!'
        if not curtain_dict['open']:
            curtain_status = 'closed'
        else:
            curtain_status = 'open'
        self.render('index.html', status=status, curtain_status=curtain_status)

class CurtainCloseHandler(tornado.web.RequestHandler):
    def get(self):
        while curtain_dict['busy']:
            pass
        curtain_close()
        status = 'Curtain is now closed!'
        if not curtain_dict['open']:
            curtain_status = 'closed'
        else:
            curtain_status = 'open'
        self.render('index.html', status=status, curtain_status=curtain_status)

class ImageHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-cache")

# urls = [(r"/", IndexHandler),(r"/open", CurtainOpenHandler),(r"/close", CurtainCloseHandler),(r"/(pic.png)", tornado.web.StaticFileHandler, {'path':'./'})]
settings = {"debug": True,}
urls = [(r"/", IndexHandler),(r"/open", CurtainOpenHandler),(r"/close", CurtainCloseHandler),(r"/(cap.jpeg)", ImageHandler, {'path':'./'}),]
def web_server(curtain_dict):
    print('server starts')
    tornado.options.parse_command_line()
    app = tornado.web.Application(urls, **settings)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    # web_server()
    pass