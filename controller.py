from tornado.web import RequestHandler


class Controller(RequestHandler):
    models = None
    processing = None
