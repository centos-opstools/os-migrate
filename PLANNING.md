## Architecture thoughts

- There should be a single entry point for authentication.  We should
  use something like [os_client_config][] to manage credentials and
  create clients.

- Can we separate export/import actions?  E.g., first export data from
  source cloud environment into a directory:

        os-migrate --cloud src_cloud --datadir mydatadir export

    And then import that data into the target cloud:

        os-migrate --cloud dest_cloud --datadir mydatadir import

    The advantage to this model is that it does not require the
    ability to connect to both environments from the same location.
    Actually moving data around this way (volumes, images) might be
    tricky. Maybe we just export the metadata and a separate command
    takes care of actual data movement?

- Can we used a plugin model for what we export/import?  E.g., use
  something like [stevedore][] to look up available datasource
  drivers.

[os_client_config]: https://github.com/openstack/os-client-config
[stevedore]: https://pypi.python.org/pypi/stevedore
