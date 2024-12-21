from django import forms
from virtualization.forms import VirtualMachineForm
import logging

logger = logging.getLogger('netbox.netbox_memory_input')
logger.setLevel(logging.DEBUG)


logger.debug("MemoryGBVirtualMachineForm module loaded")

class MemoryGBVirtualMachineForm(VirtualMachineForm):
    # Override both memory and disk fields
    memory = forms.FloatField(
        required=False,
        label='Memory (GB)',
        min_value=0.1,  # Allow sub-GB values
        widget=forms.NumberInput(attrs={'placeholder': 'Enter memory in GB'})
    )
    
    disk = forms.FloatField(
        required=False,
        label='Disk (GB)',
        min_value=0.1,  # Allow sub-GB values
        widget=forms.NumberInput(attrs={'placeholder': 'Enter disk size in GB'})
    )

    def __init__(self, *args, **kwargs):
        logger.debug("MemoryGBVirtualMachineForm initialization started")
        super().__init__(*args, **kwargs)
            
        # Handle memory conversion
        if self.instance and self.instance.memory:
            gb_value = round(self.instance.memory / 1000, 2)  # Round to 2 decimal places
            logger.debug(f"Setting initial memory value: {self.instance.memory}MB -> {gb_value}GB")
            self.initial['memory'] = gb_value
            
        # Handle disk conversion
        if self.instance and self.instance.disk:
            gb_value = round(self.instance.disk / 1000, 2)  # Round to 2 decimal places
            logger.debug(f"Setting initial disk value: {self.instance.disk}MB -> {gb_value}GB")
            self.initial['disk'] = gb_value

    def clean_memory(self):
        memory = self.cleaned_data.get('memory')
        if memory is not None:
            memory_mb = int(memory * 1000)
            logger.debug(f"Converting memory {memory}GB to {memory_mb}MB")
            return memory_mb
        return None

    def clean_disk(self):
        disk = self.cleaned_data.get('disk')
        if disk is not None:
            disk_mb = int(disk * 1000)
            logger.debug(f"Converting disk {disk}GB to {disk_mb}MB")
            return disk_mb
        return None