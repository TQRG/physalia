"""Module with util functions to use with Monsoon."""

import usb.core
from math import isclose
from Monsoon import Operations
import click

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

def get_voltage(monsoon):
    """Get voltage in the output of Monsoon."""
    read_voltage = monsoon.Protocol.getValue(Operations.OpCodes.setMainVoltage,1)
    return read_voltage / Operations.Conversion.FLOAT_TO_INT

def set_voltage_if_different(monsoon, voltage):
    """Set monsoon voltage only if it is different."""
    previous_voltage = get_voltage(monsoon)
    if not isclose(previous_voltage, voltage, abs_tol=0.0001):
        click.secho('setting voltage {} (previous was {})'.format(voltage, previous_voltage), fg='red')
        monsoon.setVout(voltage)
