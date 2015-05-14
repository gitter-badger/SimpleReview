#
# -*- coding: utf-8 -*-

import time

import whatthepatch

import pysvn2

from AbstractController import AbstractController


class SourceCode(object):
    def __init__(self, text, tab_replace=True):
        self.text = text
        self.tab_replace = tab_replace
        #
        self.__lines = []
        self.__class = []
        #
        self.default_text = None
        self.default_class = "regular"
        #
        self.__prepare(text)

    def get_line_count(self):
        return len(self.__lines)

    def set_line_count(self, capacity):
        count = len(self.__lines)
        require = capacity - count
        for _ in xrange(require):
            self.__lines.append(self.default_text)
            self.__class.append(self.default_class)

    def set_line_text(self, num, text):
        if self.tab_replace is True:
            text = text.replace("\t", "    ")
        self.__lines[num] = text

    def get_line_text(self, num):
        return self.__lines[num]

    def set_line_class(self, num, cls):
        self.__class[num] = cls

    def get_line_class(self, num):
        return self.__class[num]

    def __prepare(self, text):
        lines = text.split("\n")
        #
        self.set_line_count(len(lines) + 1)
        #
        num = 1
        for line in lines:
            self.set_line_text(num, line)
            num += 1


class RevisionViewController(AbstractController):

    def __change_color(self, orig_src, new_src, diff):
        # Step 1. Parsing patch
        diff_list = whatthepatch.parse_patch(diff)
        # Step 2. Iterate each of patch file (it may be more than one)
        for diff in diff_list:
            for s, d, v in diff.changes:
                # Step 1. Orig have no line (Insert new line)
                if s is None:
                    new_src.set_line_class(d, "bg-success")
                # Step 2. New habe no line (Remove exist line)
                elif d is None:
                    orig_src.set_line_class(s, "bg-danger")
                # Step 3. Other change
                elif s != d:
                    orig_src.set_line_class(s, "bg-info")
                    new_src.set_line_class(d, "bg-info")
                elif s == d:
                    pass
                else:
                    pass

    def service(self, req, resp):
        project_id = req.getAttribute('project')
        print project_id
        context = self.get_context()
        project_mapper = context.get_mapper("project")
        project = project_mapper.findById(project_id)
        print "Project: {project!r}".format(project=project)
        repository_root = project.get_repository_root()
        repository_absolute_url = project.get_repository_absolute_url()
        print "Absolute URL: {url!r}".format(url=repository_absolute_url)
        svn_client = pysvn2.SVNClient(repository_root=repository_absolute_url)
        #
        start = time.time()
        revision = req.getAttribute("revision")
        target = req.getParameter("target")
        #
        revision_start = revision-1
        revision_end = revision
        #
        orig = svn_client.cat(revision=revision_start, target=target)
        new = svn_client.cat(revision=revision_end, target=target)
        #
        orig_src = SourceCode(orig.content)
        new_src = SourceCode(new.content)
        #
        svn_diff = svn_client.diff(revision="{start}:{end}".format(start=revision_start, end=revision_end), target=target)
        self.__change_color(orig_src, new_src, svn_diff.diff)
        end = time.time()
        #
        params = {}
        params["target"] = target
        params["svn_time"] = "{age:.2f}".format(age=end - start)
        params["revision_start"] = revision_start
        params["revision_end"] = revision_end
        params["orig_src"] = orig_src
        params["new_src"] = new_src
        #
        #
        resp.content = self.render("revision_view.jinja2", params)
