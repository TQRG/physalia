"""Module with util functions to use with Monsoon."""

import usb.core
from  Monsoon.pmapi import USB_protocol

def _device_matcher(d):
    """Method copied from official Monsoon API"""
    try:
        return d.idVendor == 0x2AB9 and d.idProduct == 0x0001
    except:
        return False

def is_monsoon_available():
    """Check wheter there is a Monsoon connnected."""
    device = usb.core.find(custom_match=_device_matcher)
    return device is not None
