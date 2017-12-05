from __future__ import print_function
from __future__ import absolute_import

import cliff.app
import cliff.commandmanager
import logging
import openstack
import os_client_config
import stevedore
import sys

import os_migrate


class OSMigrate(cliff.app.App):
    def __init__(self):
        self.occ = os_client_config.OpenStackConfig()
        self.ds = stevedore.extension.ExtensionManager(
            'openstack.migrate.datasource',
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

        p.add_argument('--list-drivers',
                       action='store_true',
                       help='List available migration drivers')
        p.add_argument('--datadir', '-D',
                       default='.',
                       help='Specify location of data to import or export')
        p.add_argument('--drivers',
                       type=lambda x: x.split(','),
                       default=[],
                       help='Enable only specific drivers')

        # This adds all the openstack authentcation command line options
        self.occ.register_argparse_arguments(p, sys.argv)

        return p

    @property
    def sdk(self):
        if hasattr(self, '_sdk'):
            return self._sdk

        cloud = self.occ.get_one_cloud(argparse=self.options)
        _sdk = openstack.connection.from_config(cloud_config=cloud)
        self._sdk = _sdk

        return _sdk


def main(argv=sys.argv[1:]):
    app = OSMigrate()
    app.run(argv)
