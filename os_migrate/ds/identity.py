from __future__ import print_function
from __future__ import absolute_import

import os_migrate.ds.base as base


class Datasource (base.Datasource):

    description = '''Migration driver for the identity service (Keystone)'''

    def store(self):
        resources = {}

        self.export_projects(resources)
        self.export_users(resources)

        return resources

    def load(self, resources):
        for rtype, rdata in resources.items():
            importfunc = getattr(self, 'import_{}'.format(rtype), None)
            if importfunc is None:
                self.log.warn('not able to import %s data', rtype)
                continue

    def export_projects(self, resources):
        projects = resources['projects'] = []
        for project in self.sdk.identity.projects():
            projects.append(project.to_dict())

    def export_roles(self, resources):
        roles = resources['roles'] = []
        for user in self.sdk.identity.roles():
            roles.append(user.to_dict())

    def export_users(self, resources):
        users = resources['users'] = []
        for user in self.sdk.identity.users():
            users.append(user.to_dict())
