#
# -*- coding: utf-8 -*-


class ProjectModel(object):
    def __init__(self, oid=None, alias=None, name=None, url=None, target=None):
        self.oid = oid
        self.alias = alias
        self.name = name
        self.url = url
        self.target = target

    def get_repository_root(self):
        return self.url

    def get_target(self):
        return self.target

    def get_repository_absolute_url(self):
        repository_root = self.get_repository_root()
        target = self.get_target()
        #
        result = "{repository_root}/{target}".format(repository_root=repository_root.rstrip('/'), target=target.lstrip('/'))
        #
        return result

    def __repr__(self):
        return "<ProjectModel oid={oid!r} name={name!r} url={url!r} target={target!r}>".format(oid=self.oid, name=self.name, url=self.url, target=self.target)
