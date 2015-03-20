#!/usr/bin/env python
#Simple File Server
#Moises Sacal
import tornado.web
import tornado.httpserver
import os
import urllib

APP_PATH = os.path.dirname(os.path.realpath(__file__))

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/files/(.*)", DownloadHandler),
            (r"/settings/(.*)", SettingsHandler),
        ]
        settings = {
            "debug":False,
            "static_path": os.path.join(APP_PATH, "static")
        }
        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        items = []
        for filename in os.listdir(os.path.join(APP_PATH, "files")):
            items.append(filename)
        settings = []
        for filename in os.listdir(os.path.join(APP_PATH, "settings")):
            settings.append(filename)
        self.render('index.html', items=items, settings=settings)

class DownloadHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, file_name):
        file = urllib.unquote(file_name)
        print file
        x = open(os.path.join(os.path.join(APP_PATH, "files"), file))
        self.set_header('Content-Disposition', 'attachment; filename=\"' + file+'\"')
        self.finish(x.read())

class SettingsHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, file_name):
        file = urllib.unquote(file_name)
        print file
        x = open(os.path.join(os.path.join(APP_PATH, "settings"), file))
        self.set_header('Content-Disposition', 'attachment; filename=\"' + file+'\"')
        self.finish(x.read())

def main():
    applicaton = Application()
    http_server = tornado.httpserver.HTTPServer(applicaton)
    http_server.listen(8080)
    print APP_PATH

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()