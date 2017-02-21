from __future__ import print_function,absolute_import

from . import base

class Datasource (base.Datasource):

    description = '''Migration driver for the image service (Glance)'''

    def export(self):
        resources = {}

        self.export_images(resources)

        return resources

    def export_images(self, resources):
        images = resources['images'] = []
        for image in self.sdk.image.images():
            images.append(image.to_dict())
