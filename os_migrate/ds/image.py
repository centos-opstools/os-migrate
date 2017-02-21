from __future__ import print_function
from __future__ import absolute_import

import os_migrate.ds.base as base


class Datasource (base.Datasource):

    description = '''Migration driver for the image service (Glance)'''

    def store(self):
        resources = {}

        self.export_images(resources)

        return resources

    def export_images(self, resources):
        images = resources['images'] = []
        for image in self.sdk.image.images():
            images.append(image.to_dict())
