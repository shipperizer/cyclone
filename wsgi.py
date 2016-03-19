from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from cyclone.app import create_app

http_server = HTTPServer(WSGIContainer(create_app()))
http_server.listen(5000)
IOLoop.instance().start()
