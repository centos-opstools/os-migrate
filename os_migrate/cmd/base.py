import logging

class MigrateCommand(object):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger('{}.{}'.format(
            self.__module__,
            self.__class__.__name__))
        super(MigrateCommand, self).__init__(*args, **kwargs)

    @property
    def ds(self):
        try:
            # os-migrate
            return self.app.ds
        except AttributeError:
            # oc
            return self.app.client_manager.migrate.ds

    @property
    def sdk(self):
        try:
            # os-migrate
            return self.app.sdk
        except AttributeError:
            # oc
            return self.app.client_manager.migrate.sdk
