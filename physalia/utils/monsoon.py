"""Module with util functions to use with Monsoon."""

import os
import sys

def is_monsoon_available():
    """Check wheter there is a Monsoon connnected."""
    for dev in os.listdir("/dev"):
        prefix = "ttyACM"
        # Prefix is different on Mac OS X.
        if sys.platform == "darwin":
            prefix = "tty.usbmodem"
        if dev.startswith(prefix):
            return True
    return False
