#
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader

from ConnectionPool import ConnectionPool
from sr.models.ProjectMapper import ProjectMapper


class Context(object):
    def __init__(self):
        self.__env = Environment(loader=FileSystemLoader('resources/views'))
        self.__env.filters['code_escape'] = self.__code_escape
        self.__mappers = {}
        self.__mappers["project"] = ProjectMapper(context=self)
        self.__config = {
            "pool_name": "code-review",
            "pool_size": 15,

            "user": "root",
            "password": "1111",
            "host": "127.0.0.1",
            "port": 3306,
            "database": "simple_review",
            "connection_timeout": 5.0,
        }
        self.__pool = ConnectionPool(config=self.__config)

    def __code_escape(self, val):
        result = val[::].decode("cp1251", errors='replace')
        result = result.replace(u"<", u"&lt;")
        result = result.replace(u">", u"&gt;")
        #result = result.replace(">", "&gt;")
        return result


    def get_mapper(self, name):
        return self.__mappers.get(name)

    def get_pool(self):
        return self.__pool

    def get_env(self):
        return self.__env
