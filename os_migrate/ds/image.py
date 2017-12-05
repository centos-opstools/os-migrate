from __future__ import print_function
from __future__ import absolute_import

import json
import fnmatch
import os
import tempfile

import os_migrate.ds.base as base

class Datasource (base.Datasource):

    description = '''Migration driver for the image service (Glance)'''

    @classmethod
    def register_argparse_arguments(cls, parser):
        g = parser.add_argument_group('image datasource')
        g.add_argument('--include-image-data',
                            action='store_true',
                            help='export or import the contents of images')
        g.add_argument('--exclude-image-names',
                       action='append',
                       default=[],
                       help='exclude images with names matching specified '
                       'glob pattern')
        g.add_argument('--include-image-names',
                       action='append',
                       default=[],
                       help='include images with names matching specified '
                       'glob pattern')

    def store(self):
        self.create_datadir()
        self.export_images()

    def export_images(self):
        images = []
        for image in self.sdk.image.images():
            exclude = None
            include = None

            if self.app.options.exclude_image_names:
                exclude = False
                for pattern in self.app.options.exclude_image_names:
                    if fnmatch.fnmatch(image.name, pattern):
                        exclude = True
                        break

            if self.app.options.include_image_names:
                include = False
                for pattern in self.app.options.include_image_names:
                    if fnmatch.fnmatch(image.name, pattern):
                        include = True
                        break

            if exclude:
                self.log.debug('skipping image %s (%s): '
                               'matched exclude pattern',
                               image.name, image.id)
                continue

            if include is False:
                self.log.debug('skipping image %s (%s): '
                               'did not match include pattern',
                               image.name, image.id)
                continue

            images.append(image.to_dict())

            if self.app.options.include_image_data:
                self.export_image_data(image)

        with self.open('images.json', 'w') as fd:
            json.dump(images, fd)

    def load(self, resources):
        raise NotImplementedError('load')

    def export_image_data(self, image):
        self.log.info('downloading data for image %s (%s)',
                      image.name, image.id)

        with tempfile.NamedTemporaryFile(
                dir=self.app.options.datadir,
                prefix='tmp.image') as outfd:

            url = '/'.join([
                image.base_path, image.id, 'file'])
            res = self.app.sdk.image.session.get(
                url,
                stream=True,
                endpoint_filter=image.service)

            res.raise_for_status()
            for chunk in res.iter_content(chunk_size=1024):
                outfd.write(chunk)

            datafile = os.path.join(
                self.datadir,
                'image.{}'.format(image.id))
            os.link(outfd.name, datafile)
