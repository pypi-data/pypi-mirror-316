from netbox.plugins import PluginConfig

class NetboxAutoNamesConfig(PluginConfig):
    name = 'netbox_autonames'
    verbose_name = 'NetBoxAutoNames'
    version = '0.4.2'
    description = 'Auto-generate names for devices and VMs based on their role.'
    base_url = ''
    required_settings = []
    min_version = '2.10.0'

    def ready(self):
        import netbox_autonames.signals
        
        # Import and override the form inside ready()
        from virtualization.forms import VirtualMachineForm
        from netbox_autonames.forms import CustomVirtualMachineForm
        import virtualization.forms
        virtualization.forms.VirtualMachineForm = CustomVirtualMachineForm

config = NetboxAutoNamesConfig