#
# -*- coding: utf-8 -*-

import time

from sr.AbstractController import AbstractController
from models.ProjectModel import ProjectModel

class WelcomeController(AbstractController):

    def service(self, req, resp):
        # Step 1. Populate project
        context = self.get_context()
        project_mapper = context.get_mapper('project')
        items = project_mapper.findAll()


        # Step 2. Render image
        params = {}
        params["items"] = items
        start = time.time()
        resp.content = self.render("welcome.jinja2", params=params)
        end = time.time()
        print end - start
