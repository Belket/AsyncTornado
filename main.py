from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.web import StaticFileHandler
from handlers import MainHandler, FileHandler
from models import Models
from processing import ProcessingMethods
from controller import Controller
import os

models_object = Models()
processing_object = ProcessingMethods()
Controller.models = models_object
Controller.processing = processing_object

html_path = os.path.join(os.path.dirname(__file__), "static/html")
css_path = os.path.join(os.path.dirname(__file__), "static/css")
js_path = os.path.join(os.path.dirname(__file__), "static/js")
img_path = os.path.join(os.path.dirname(__file__), "static/img")
assets_path = os.path.join(os.path.dirname(__file__), "static/assets")

application = Application(
    [(r'(favicon.ico)', StaticFileHandler, {"path": img_path}),
     ("/", MainHandler),
     ("/upload_file", FileHandler)],
    template_path=html_path, static_path=os.path.join(os.path.dirname(__file__), "static"),)

server = HTTPServer(application)
server.listen(7000)
print("Server was started on port ", 7000)
IOLoop.current().start()

