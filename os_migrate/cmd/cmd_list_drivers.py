from __future__ import print_function
from __future__ import absolute_import

import cliff.lister

class Command(cliff.lister.Lister):

    def take_action(self, parsed_args):
        header = ['name', 'description', 'enabled']
        rows = []

        for ds in self.app.ds:
            enabled = ((not self.app.options.drivers)
                       or (ds.name in self.app.options.drivers))

            rows.append([ds.name, ds.plugin.description, enabled])

        return (header, rows)

