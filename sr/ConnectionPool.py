#
# -*- coding: utf-8 -*-

import mysql.connector


class ConnectionPool(object):
    def __init__(self, size=5, config=None):
        if not isinstance(config, dict):
            raise ValueError("Connection parameters")
        self.__size = size
        self.__connections = []
        self.__config = config

    def dispose(self):
        while self.__connections > 0:
            cnx = self.__connections.pop()
            cnx.close()

    def prepare(self):
        """ Populate pool values
        """
        #
        for num in xrange(self.__size):
            cnx = self.__create_connection()
            self.__connections.append(cnx)

    def __create_connection(self):
        prepare_config = self.__config.copy()
        cnx = mysql.connector.connect(**prepare_config)
        return cnx

    def acquire(self):
        if len(self.__connections) > 0:
            cnx = self.__connections.pop()
        else:
            cnx = self.__create_connection()
        return cnx

    def release(self, cnx):
        self.__connections.append(cnx)
