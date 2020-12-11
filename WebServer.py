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
        id = self.get_argument("id", 0)

        # sensor数据
        sensor_data = 0
        wifi_sniffer_count = 0

        self.write("WIFI sniffer:" + str(wifi_sniffer_count))
        self.write('\n' + 'Sensor Reading:' + str(sensor_data))

urls = [(r"/", IndexHandler),]

def web_server():
    tornado.options.parse_command_line()
    app = tornado.web.Application(urls)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
    print('server starts')

if __name__ == "__main__":
    web_server()