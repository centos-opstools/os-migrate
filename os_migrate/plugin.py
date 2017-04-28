
from __future__ import print_function
from __future__ import absolute_import

import logging
from openstack import connection
import os
import os_client_config
import stevedore
import sys


API_NAME = 'migrate'
API_VERSION_OPTION = 'os_migrate_api_version'
API_DEFAULT_VERSION = 1
API_VERSIONS = {
    '1': 'os_migrate.plugin.OSMigrateClient',
}


def build_option_parser(parser):
    '''Hook to add global options to the parser'''
    parser.add_argument(
        '--os-migrate-api-version',
        metavar='<migrate-api-version>',
        default=os.environ.get('OS_MIGRATE_API_VERSION', API_DEFAULT_VERSION),
        help=('Migrate API version, default={} '
              '(Env: OS_MIGRATE_API_VERSION)'.format(API_DEFAULT_VERSION)))
    parser.add_argument(
        '--datadir', '-D',
        default='.',
        help='Specify location of data to import or export')
    parser.add_argument(
        '--drivers',
        type=lambda x: x.split(','),
        default=[],
        help='Enable only specific drivers')
    return parser


def make_client(instance):
    '''Hook to create the client object'''
    return OSMigrateClient(instance)


class OSMigrateClient(object):
    def __init__(self, instance):
        self._instance = instance
        self.occ = os_client_config.OpenStackConfig()
        self.ds = stevedore.extension.ExtensionManager(
            'openstack.migrate.datasource',
        )

    @property
    def sdk(self):
        if not hasattr(self, '_sdk'):
            self._sdk = connection.Connection(
                            authenticator=self._instance.session.auth,
                            verify=self._instance.session.verify,
                            cert=self._instance.session.cert)
        return self._sdk
