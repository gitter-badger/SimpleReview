#
# -*- coding: utf-8 -*-


import abc

from bottle import request


class HTTPRequest(object):
    def __init__(self):
        self.__attributes = {}

    def getAttribute(self, name):
        result = None
        if name in self.__attributes:
            result = self.__attributes[name]
        return result

    def setAttribute(self, name, value):
        self.__attributes[name] = value

    def getParameter(self, name):
        if name not in request.query:
            raise EnvironmentError("No variable")
        result = request.query[name]
        return result


class HTTPResponse(object):
    def __init__(self):
        self.content = None


class AbstractController(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, context):
        self._context = context

    def get_context(self):
        return self._context

    def serve(self, **kwargs):
        req = HTTPRequest()
        resp = HTTPResponse()
        #
        for k,v in kwargs.items():
            req.setAttribute(k, v)
        #
        self.service(req, resp)
        #
        return resp.content

    @abc.abstractmethod
    def service(self, req, resp):
        pass

    def render(self, view_name, params):
        context = self.get_context()
        env = context.get_env()
        templ = env.get_template(view_name)
        content = templ.render(**params)
        return content
