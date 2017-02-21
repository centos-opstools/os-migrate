from __future__ import print_function,absolute_import

from . import base

class Datasource (base.Datasource):

    description = '''Migration driver for the compute service (Nova)'''

    def export(self):
        resources = {}

        self.export_keypairs(resources)
        self.export_flavors(resources)

        return resources

    def export_keypairs(self, resources):
        keypairs = resources['keypairs'] = []
        for keypair in self.sdk.compute.keypairs():
            keypairs.append(keypair.to_dict())

    def export_flavors(self, resources):
        flavors = resources['flavors'] = []
        for flavor in self.sdk.compute.flavors():
            flavors.append(flavor.to_dict())
