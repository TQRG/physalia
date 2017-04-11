"""Module with util functions to control Android devices."""

import subprocess

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
