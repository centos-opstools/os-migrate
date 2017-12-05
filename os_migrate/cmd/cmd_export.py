from __future__ import print_function
from __future__ import absolute_import

import os
import json
import cliff.command
import os_migrate.cmd.base as base

class Command(base.LoggingCommand, cliff.command.Command):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def take_action(self, parsed_args):
        datadir = os.path.abspath(self.app.options.datadir)
        self.log.info('starting export of openstack data to %s',
                      datadir)

        for ds in self.app.ds:
            enabled = ((not self.app.options.drivers)
                       or (ds.name in self.app.options.drivers))
            if not enabled:
                self.log.debug('skipping %s: disabled', ds.name)
                continue

            dumper = ds.plugin(self.app.sdk)

            self.log.info('exporting %s data', ds.name)
            datafile = os.path.join(datadir, '{}.json'.format(ds.name))
            resources = dumper.store()
            with open(datafile, 'w') as fd:
                json.dump(resources, fd, indent=2)

        self.log.info('finished export')
