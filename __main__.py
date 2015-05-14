#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import bottle

from sr.Context import Context

from sr.AdminController import AdminController
from sr.HistoryController import HistoryController
from sr.RevisionController import RevisionController
from sr.RevisionViewController import RevisionViewController
from sr.WelcomeController import WelcomeController


class Application(object):
    def run(self):
        self.__bottle = bottle.Bottle()
        #
        context = Context()
        #
        self.__bottle.add_route(bottle.Route(app=self.__bottle, rule="/", method="GET", callback=WelcomeController(context).serve))
        self.__bottle.add_route(bottle.Route(app=self.__bottle, rule="/admin", method="GET", callback=AdminController(context).serve))
        self.__bottle.add_route(bottle.Route(app=self.__bottle, rule="/admin", method="POST", callback=AdminController(context).serve))
        self.__bottle.add_route(bottle.Route(app=self.__bottle, rule="/project/<project:int>/revision/<revision:int>", method="GET", callback=RevisionController(context).serve))
        self.__bottle.add_route(bottle.Route(app=self.__bottle, rule="/project/<project:int>/revision/<revision:int>/view", method="GET", callback=RevisionViewController(context).serve))
        self.__bottle.add_route(bottle.Route(app=self.__bottle, rule="/project/<project:int>/history", method="GET", callback=HistoryController(context).serve))
        #
        self.__bottle.run(host='0.0.0.0', port=8040, debug=True)


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    sys.exit(main())
