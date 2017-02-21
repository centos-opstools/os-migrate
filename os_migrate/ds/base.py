from __future__ import print_function,absolute_import

import abc
import six

@six.add_metaclass(abc.ABCMeta)
class Datasource(object):
    def __init__(self, sdk):
        self.sdk = sdk
