# os-migrate: tools for migrating between OpenStack clouds

## Examples

### List available migration drivers

    os-migrate-export --list-drivers

### Export data from a cloud

This will use the configuration for a cloud named `undercloud` from
your `clouds.yaml` file, which can be located in your current working
directory, in `$HOME/.config/openstack/clouds.yaml`, or in
`/etc/openstack.clouds.yaml`.

A `clouds.yaml` file looks something like:

    clouds:
      undercloud:
        identity_interface: admin
        identity_api_version: 3
        auth:
          password: SECRET
          auth_url: https://192.168.24.2:13000/v2.0
          username: admin
          tenant_name: admin

Once you have a `clouds.yaml` file in place, you can export data from
your cloud with a command like:

    $ mkdir mydata
    $ os-migrate-export --os-cloud undercloud -D mydata -v

Which will produce the following output:

    INFO:os_migrate.cmd.export:starting export of openstack data to /home/stack/os-migrate/data
    INFO:os_migrate.cmd.export:exporting image data
    INFO:os_migrate.cmd.export:exporting compute data
    INFO:os_migrate.cmd.export:exporting identity data
    INFO:os_migrate.cmd.export:finished export

And a collection of files in your `mydata` directory:

    $ ls mydata
    compute.json  identity.json  image.json
