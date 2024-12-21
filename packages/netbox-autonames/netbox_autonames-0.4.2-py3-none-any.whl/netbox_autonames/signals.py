from django.db.models.signals import pre_save
from django.dispatch import receiver
from dcim.models import Device
from django.conf import settings
import logging
import re
from .forms import get_next_shared_number

logger = logging.getLogger('netbox.netbox_autonames')

@receiver(pre_save, sender=Device)
def auto_generate_device_name(sender, instance, **kwargs):
    try:
        if not instance.name:
            role = instance.role.slug
            config = settings.PLUGINS_CONFIG.get('netbox_autonames', {})
            device_map = config.get('DEVICE_NAME_MAP', {})
            
            if role in device_map:
                role_config = device_map[role]
                if isinstance(role_config, str):
                    prefix = role_config
                    exceptions = []
                    shared_with_vms = False
                else:
                    prefix = role_config['prefix']
                    exceptions = role_config.get('exceptions', [])
                    shared_with_vms = role_config.get('shared_sequence_with_vms', False)
                
                if shared_with_vms:
                    # Use shared numbering for servers
                    instance.name = get_next_shared_number(prefix, exceptions)
                else:
                    # Use device-only numbering for other types
                    existing_devices = Device.objects.filter(
                        name__iregex=f'^{re.escape(prefix)}\d+$'
                    )
                    
                    max_num = 0
                    for device in existing_devices:
                        match = re.match(f'^{re.escape(prefix)}(\d+)$', device.name, re.IGNORECASE)
                        if match:
                            num = int(match.group(1))
                            if num > max_num:
                                max_num = num
                    
                    next_num = max_num + 1
                    while str(next_num) in exceptions:
                        next_num += 1
                        
                    instance.name = f"{prefix}{next_num:04d}"
                    
    except Exception as e:
        logger.error(f"Error in auto_generate_device_name: {str(e)}", exc_info=True)
