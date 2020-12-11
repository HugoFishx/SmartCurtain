#! /usr/bin/python
# encoding:utf-8

# 导入Tornado模块
import tornado.ioloop
import tornado.httpserver
import tornado.web
import tornado.options

from tornado.options import define, options

define("port", type=int, default=8000, help="run on the given port")

class IndexHandler(tornado.web.RequestHandler):
    def get(self):


        # sensor数据
        sensor_data = 0
        wifi_sniffer_count = 0

        re

urls = [(r"/", IndexHandler),]

def main():
    tornado.options.parse_command_line()
    app = tornado.web.Application(urls)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()