#-*- coding:utf-8 -*-
import web
from handle import Handle

urls = (
    '/wx', 'Handle',
)

app = web.application(urls, globals()).wsgifunc()
from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)
