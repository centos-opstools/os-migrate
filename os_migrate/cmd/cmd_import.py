from __future__ import print_function
from __future__ import absolute_import

import argparse
import json
import logging
import openstack
import os
import os_client_config
import stevedore
import sys

LOG = logging.getLogger(__name__)
occ = os_client_config.OpenStackConfig()


def parse_args():
    p = argparse.ArgumentParser()

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
    occ.register_argparse_arguments(p, sys.argv)

    g = p.add_argument_group('Logging options')
    g.add_argument('--verbose', '-v',
                   action='store_const',
                   const=logging.INFO,
                   dest='loglevel')
    g.add_argument('--debug', '-d',
                   action='store_const',
                   const=logging.DEBUG,
                   dest='loglevel')

    p.set_defaults(loglevel=logging.WARNING)

    return p.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=args.loglevel)

    mgr = stevedore.extension.ExtensionManager(
        'openstack.migrate.datasource',
    )

    if args.list_drivers:
        print('Available migration drivers:')
        print()
        for ext in mgr:
            enabled = ((not args.drivers) or (ext.name in args.drivers))
            print('{:10}: {} ({})'.format(
                ext.name,
                ext.plugin.description,
                'enabled' if enabled else 'disabled'
            ))
        return

    cloud = occ.get_one_cloud(argparse=args)
    sdk = openstack.connection.from_config(cloud_config=cloud)

    datadir = os.path.abspath(args.datadir)
    LOG.info('starting import of openstack data from {}'.format(datadir))
    for ext in mgr:
        enabled = ((not args.drivers) or (ext.name in args.drivers))
        if not enabled:
            LOG.debug('skipping %s: disabled', ext.name)
            continue

        datafile = os.path.join(datadir, '{}.json'.format(ext.name))
        if not os.path.exists(datafile):
            LOG.debug('skipping %s: no datafile', ext.name)
            continue

        loader = ext.plugin(sdk)
        if not hasattr(loader, 'load'):
            LOG.debug('skipping %s: no load method', ext.name)
            continue

        with open(datafile, 'r') as fd:
            LOG.info('importing {} data'.format(ext.name))
            data = json.load(fd)
            loader.load(data)

    LOG.info('finished import')
