from netbox.plugins import PluginConfig

class NetboxTopologyButton(PluginConfig):
    name = 'netbox_topology_plugin_button'
    verbose_name = ' NetBox Topology Button'
    description = 'Adds a Button to the device Page to directly jump to a filtered topology view.'
    version = '0.1'
    base_url = 'topology-button'
    min_version = '4.0.0'

config = NetboxTopologyButton
