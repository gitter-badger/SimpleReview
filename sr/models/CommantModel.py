#
# -*- coding: utf-8 -*-


class CommentModel(object):
    def __init__(self, oid=None, project_id=None, author=None, msg=None):
        self.oid = oid
        self.project_id = project_id
        self.author = author
        self.msg = msg

