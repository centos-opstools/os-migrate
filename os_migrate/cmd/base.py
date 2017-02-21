import logging

class LoggingCommand(object):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger('{}.{}'.format(
            self.__module__,
            self.__class__.__name__))

        super(LoggingCommand, self).__init__(*args, **kwargs)
