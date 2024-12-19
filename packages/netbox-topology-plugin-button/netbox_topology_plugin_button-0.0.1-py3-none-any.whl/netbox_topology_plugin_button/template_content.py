from netbox.plugins import PluginTemplateExtension

class TopologyButtonView(PluginTemplateExtension):
    model = "dcim.device"

    def buttons(self):
        return self.render("netbox_topology_plugin_button/TopologyButton.html")

template_extensions = [TopologyButtonView]
