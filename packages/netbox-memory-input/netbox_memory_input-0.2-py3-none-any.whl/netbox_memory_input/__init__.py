from netbox.plugins import PluginConfig

class NetboxMemoryInputConfig(PluginConfig):
    name = 'netbox_memory_input'
    verbose_name = 'NetBox Memory Input'
    description = 'Input VM memory in GB instead of MB'
    version = '0.1'
    base_url = ''
    required_settings = []
    min_version = '2.10.0'
    
    def ready(self):
        from . import forms
        import virtualization.forms
        virtualization.forms.VirtualMachineForm = forms.MemoryGBVirtualMachineForm
config = NetboxMemoryInputConfig

