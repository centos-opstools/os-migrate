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
