from __future__ import print_function
from __future__ import absolute_import

import abc
import logging
import six


@six.add_metaclass(abc.ABCMeta)
class Datasource(object):
    def __init__(self, sdk):
        self.sdk = sdk
        self.log = logging.getLogger('{}.{}'.format(
            self.__module__,
            self.__class__.__name__))

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
