#
# -*- coding: utf-8 -*-


from sr.models.ProjectModel import ProjectModel


class ProjectMapper(object):
    def __init__(self, context):
        self.__context = context

    def findById(self, project_id):
        result = None
        pool = self.__context.get_pool()
        conn = None
        ctx = None
        try:
            conn = pool.acquire()
            ctx = conn.cursor()
            ctx.execute("SELECT `id`, `alias`, `name`, `url`, `target` FROM `project` WHERE `id` = %(project_id)s", {"project_id": project_id})
            #
            result = []
            for o_id, o_alias, o_name, o_url, o_target in ctx:
                result = ProjectModel(oid=o_id, alias=o_alias, name=o_name, url=o_url, target=o_target)
        finally:
            if ctx is not None:
                ctx.close()
            if conn is not None:
                pool.release(conn)
        #
        return result


    def findAll(self):
        result = None
        # Step 1. Populate all project data
        pool = self.__context.get_pool()
        conn = None
        ctx = None
        try:
            conn = pool.acquire()
            ctx = conn.cursor()
            ctx.execute("SELECT `id`, `alias`, `name`, `url`, `target` FROM `project`")
            #
            result = []
            for o_id, o_alias, o_name, o_url, o_target in ctx:
                result.append(ProjectModel(oid=o_id, alias=o_alias, name=o_name, url=o_url, target=o_target))
        finally:
            if ctx is not None:
                ctx.close()
            if conn is not None:
                pool.release(conn)
        #
        return result
