from __future__ import print_function
from __future__ import absolute_import

import os
import json
import cliff.command
import os_migrate.cmd.base as base
import os_migrate.exc as exc

class Command(base.LoggingCommand, cliff.command.Command):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def take_action(self, parsed_args):
        datadir = os.path.abspath(self.app.options.datadir)
        if not os.path.exists(datadir):
            raise exc.CommandError('directory %s does not exist')

        self.log.info('starting import of openstack data from %s',
                      datadir)

        for ds in self.app.ds:
            enabled = ((not self.app.options.drivers)
                       or (ds.name in self.app.options.drivers))
            if not enabled:
                self.log.debug('skipping %s: disabled', ds.name)
                continue

            datafile = os.path.join(datadir, '{}.json'.format(ds.name))
            if not os.path.exists(datafile):
                self.log.debug('skipping %s: no data file', ds.name)
                continue

            loader = ds.plugin(self.app.sdk, self.app)

            with open(datafile, 'r') as fd:
                self.log.info('importing %s data', ds.name)
                data = json.load(fd)
                loader.load(data)

        self.log.info('finished import')
