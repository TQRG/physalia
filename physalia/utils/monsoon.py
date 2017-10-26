"""Module with util functions to use with Monsoon."""

import usb.core

def _device_matcher(device):
    """Check if device is monsoon.

    Method copied from official Monsoon API.
    """
    # pylint: disable=bare-except
    try:
        return device.idVendor == 0x2AB9 and device.idProduct == 0x0001
    except:
        return False

def is_monsoon_available():
    """Check wheter there is a Monsoon connnected."""
    device = usb.core.find(custom_match=_device_matcher)
    return device is not None
