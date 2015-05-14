#
# -*- coding: utf-8 -*-

import time

import pysvn2

from sr.AbstractController import AbstractController


class HistoryController(AbstractController):
    def service(self, req, resp):
        project_id = req.getAttribute('project')
        print project_id
        context = self.get_context()
        project_mapper = context.get_mapper("project")
        project = project_mapper.findById(project_id)
        print "Project: {project!r}".format(project=project)
        repository_absolute_url = project.get_repository_absolute_url()
        print repository_absolute_url
        #
        svn_client = pysvn2.SVNClient(repository_root=repository_absolute_url)
        #
        svn_info = svn_client.info()
        revision = int(svn_info.commit_revision)
        #
        revision_start = revision - 1000
        revision_end = revision
        start = time.time()
        svn_log = svn_client.log(revision="{revision_start}:{revision_end}".format(revision_start=revision_start, revision_end=revision_end))
        end = time.time()
        #
        params = {}
        params["project_id"] = project_id
        params["log"] = svn_log
        params["svn_time"] = "{age:.2f}".format(age=end - start)
        params["revision_start"] = revision_start
        params["revision_end"] = revision_end
        #
        resp.content = self.render("history.jinja2", params=params)
