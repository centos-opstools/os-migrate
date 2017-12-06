from __future__ import print_function
from __future__ import absolute_import

import cliff.app
import cliff.commandmanager
import logging
import os
import stevedore
import sys

import os_migrate


class OSMigrate(cliff.app.App):
    def __init__(self):
        self.ds = stevedore.extension.ExtensionManager(
            'openstack.migrate.driver',
        )

        super(OSMigrate, self).__init__(
            description='OpenStack data migration tool',
            version=os_migrate.__version__,
            command_manager=cliff.commandmanager.CommandManager(
                'openstack.migrate.command'),
            deferred_help=True)

    def build_option_parser(self, description, version, argparse_kwargs=None):
        p = super(OSMigrate, self).build_option_parser(
            description, version, argparse_kwargs=argparse_kwargs)

        g = p.add_argument_group('Migration options')
        g.add_argument('--from-cloud', '-f')
        g.add_argument('--to-cloud', '-t')

        p.set_defaults(loglevel='WARNING')

        return p

    def initialize_app(self, argv):
        cfgfile = self.find_config_file()
        self.LOG.warning('found config file: %s', cfgfile)

    def find_config_file(self):
        for dir in (os.environ.get('OS_MIGRATE_CONFIG_FILE'),
                    '.',
                    os.path.join(os.environ.get('HOME', '/'),
                                 '.config', 'openstack')):
            if dir is None:
                continue

            for ext in ('.yml', '.yaml'):
                cfgfile = os.path.join(dir, 'migrate' + ext)
                if os.path.isfile(cfgfile):
                    break
            else:
                continue

            return cfgfile

        return None


def main(argv=sys.argv[1:]):
    app = OSMigrate()
    app.run(argv)
