#
# -*- coding: utf-8 -*-

import pysvn2

from sr.AbstractController import AbstractController


class RevisionController(AbstractController):
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
        revision = req.getAttribute("revision")
        if revision is None:
            svn_info = svn_client.info()
            revision = int(svn_info.commit_revision)
        #
        revision_start = revision-1
        revision_end = revision
        #
        svn_diff = svn_client.diff_summarize(revision="{start}:{end}".format(start=revision_start, end=revision_end))
        #
        params = {}
        params["project_id"] = project_id
        params["items"] = svn_diff.paths
        params["revision_start"] = revision_start
        params["revision_end"] = revision_end
        #
        resp.content = self.render("diff_s.jinja2", params=params)
