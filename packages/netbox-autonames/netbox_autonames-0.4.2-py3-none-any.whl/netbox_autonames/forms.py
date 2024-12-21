from virtualization.forms import VirtualMachineForm
from virtualization.models import VirtualMachine
from dcim.models import Device
from django.conf import settings
import logging
import re

logger = logging.getLogger('netbox.netbox_autonames')

def get_next_shared_number(prefix, exceptions=None):
    """
    Get next available number considering both VMs and Devices
    """
    try:
        logger.debug(f"Starting get_next_shared_number with prefix: {prefix}")
        logger.debug(f"Exceptions to consider: {exceptions}")
        
        # Convert exceptions to numbers
        exception_numbers = set()
        if exceptions:
            for exc in exceptions:
                match = re.match(f'^{re.escape(prefix)}(\d+)$', exc, re.IGNORECASE)
                if match:
                    num = int(match.group(1))
                    exception_numbers.add(num)
                    logger.debug(f"Added exception number: {num}")

        # Get all VMs and Devices that match our pattern
        existing_vms = VirtualMachine.objects.filter(
            name__iregex=f'^{re.escape(prefix)}\d+$'
        )
        existing_devices = Device.objects.filter(
            name__iregex=f'^{re.escape(prefix)}\d+$'
        )
        
        logger.debug(f"Found {existing_vms.count()} matching VMs")
        logger.debug(f"Found {existing_devices.count()} matching Devices")
        
        # Find all used numbers and the highest non-exception number
        used_numbers = set()
        highest_regular_num = 0
        
        # Process VMs
        for vm in existing_vms:
            match = re.match(f'^{re.escape(prefix)}(\d+)$', vm.name, re.IGNORECASE)
            if match:
                num = int(match.group(1))
                used_numbers.add(num)
                if num not in exception_numbers and num > highest_regular_num:
                    highest_regular_num = num
                logger.debug(f"Found VM number: {num}")
        
        # Process Devices
        for device in existing_devices:
            match = re.match(f'^{re.escape(prefix)}(\d+)$', device.name, re.IGNORECASE)
            if match:
                num = int(match.group(1))
                used_numbers.add(num)
                if num not in exception_numbers and num > highest_regular_num:
                    highest_regular_num = num
                logger.debug(f"Found Device number: {num}")
                
        logger.debug(f"Current highest regular number: {highest_regular_num}")
        
        # If we have no numbers in use, start from 1
        if not highest_regular_num and not exception_numbers:
            logger.debug("No existing numbers found, starting from 1")
            return f"{prefix}0001"
            
        # Start from the number after our highest regular number
        next_num = highest_regular_num + 1
        
        # If this number is in exceptions or used, increment until we find a free one
        while next_num in exception_numbers or next_num in used_numbers:
            next_num += 1
            
        next_name = f"{prefix}{next_num:04d}"
        logger.debug(f"Generated next name: {next_name}")
        return next_name
        
    except Exception as e:
        logger.error(f"Error in get_next_shared_number: {str(e)}", exc_info=True)
        return f"{prefix}0001"

class CustomVirtualMachineForm(VirtualMachineForm):
    def __init__(self, *args, **kwargs):
        logger.debug("CustomVirtualMachineForm initialization started")
        super().__init__(*args, **kwargs)
        
        try:
            instance = kwargs.get('instance')
            is_new = not instance or not instance.pk or not instance.name
            
            if is_new:
                config = settings.PLUGINS_CONFIG.get('netbox_autonames', {})
                prefix = config.get('VM_PREFIX', 'itsrv')
                exceptions = config.get('VM_EXCEPTIONS', [])
                
                next_name = get_next_shared_number(prefix, exceptions)
                
                self.initial['name'] = next_name
                if 'name' in self.fields:
                    self.fields['name'].initial = next_name
                    
        except Exception as e:
            logger.error(f"Error in form initialization: {str(e)}", exc_info=True)
            self.initial['name'] = 'ITSRV0001'
