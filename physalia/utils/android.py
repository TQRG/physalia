"""Module with util functions to control Android devices."""

import subprocess
from whichcraft import which

def set_charging_enabled(enabled, serialno=None):
    """Enable or disable charging the device."""
    if serialno:
        command = (
            "adb shell -s {serialno} dumpsys battery set ac {enabled};"
            "adb shell -s {serialno} dumpsys battery set usb {enabled};"
        ).format(serialno=serialno, enabled=int(enabled))
    else:
        command = (
            "adb shell dumpsys battery set ac {enabled};"
            "adb shell dumpsys battery set usb {enabled}"
        ).format(enabled=int(enabled))

    subprocess.check_output(
        command,
        shell=True
    )

def install_apk(apk):
    """Install apk."""
    subprocess.check_output(["adb", "install", apk])

def check_adb():
    """Check whether adb is available."""
    return which("adb") is not None

def is_android_device_available():
    """Check whether there is at least an available android devices."""
    if not check_adb():
        return False
    result = subprocess.check_output("adb devices", shell=True)
    devices = result.partition('\n')[2].replace('\n', '').split('\tdevice')
    devices = [device for device in devices if len(device) > 2]
    return len(devices) > 0

def get_device_model(serialno=None):
    """Get the currently connected device model."""
    if serialno:
        command = ("adb shell -s {} "
                   "getprop ro.product.model").format(serialno)
    else:
        command = "adb shell getprop ro.product.model"
    try:
        return subprocess.check_output(
            command,
            shell=True
        ).strip()
    except subprocess.CalledProcessError:
        return "N/A"
    