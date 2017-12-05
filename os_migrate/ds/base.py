from __future__ import print_function
from __future__ import absolute_import

import abc
import logging
import six
import os


@six.add_metaclass(abc.ABCMeta)
class Datasource(object):
    def __init__(self, sdk, app):
        '''`sdk` is an `openstack.connection.Connection object`, and
        `app` is a cliff.app.App object.'''
        self.sdk = sdk
        self.app = app

        self.datadir = os.path.join(
            self.app.options.datadir, self.__class__.__module__)

        self.log = logging.getLogger('{}.{}'.format(
            self.__module__,
            self.__class__.__name__))

    def create_datadir(self):
        if not os.path.isdir(self.datadir):
            os.mkdir(self.datadir)

    def datadir_exists(self):
        return os.path.isdir(self.datadir)

    def open(self, path, mode='r'):
        return open(os.path.join(self.datadir, path), mode)

    @classmethod
    def register_argparse_arguments(cls, parser):
        pass

    @abc.abstractproperty
    def description(self):
        '''The `description` property should return a short
        description of the driver.'''
        pass

    @abc.abstractmethod
    def store(self):
        '''The `store` method will return a dictionary of resources.
        The contents of the dictionary are intended to be consumed by
        the `load` method.'''
        pass

    @abc.abstractmethod
    def load(self, resources):
        '''The `load` method will instantiate resources based on the
        contents of the `resources` dictionary, which was previously
        created by the `store` method.'''
        pass
