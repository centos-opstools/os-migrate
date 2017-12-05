# os-migrate: tools for migrating between OpenStack clouds

## Examples

### List available migration drivers

    os-migrate list-drivers

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

    $ mkdir data
    $ os-migrate --os-cloud undercloud -D data export

Which will produce the following output:

    starting export of openstack data to /home/stack/os-migrate/data
    exporting image data
    exporting compute data
    exporting identity data
    finished export

And a collection of files in your `data` directory:

    $ ls data
    compute.json  identity.json  image.json
