"""Module with util functions to control Android devices."""

import subprocess
import re
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

def prevent_device_from_sleep(enabled):
    """Prevent device from sleep while usb connected."""
    comand = "adb shell svc power stayon {}".format(
        {True: 'usb', False: 'false'}[enabled]
    )
    subprocess.check_output(
        comand,
        shell=True
    )

def is_screen_on():
    """Check whether the screen is on."""
    try:
        subprocess.check_output(
            "adb shell dumpsys input_method | grep mInteractive=true",
            shell=True
        )
        return True
    except subprocess.CalledProcessError:
        pass
    try:
        subprocess.check_output(
            'adb shell dumpsys power | grep "Display Power: state=ON"',
            shell=True
        )
        return True
    except subprocess.CalledProcessError:
        pass
    return False

def is_locked():
    """Check whether device is locked."""
    output = subprocess.check_output(
        "adb shell service call trust 7",
        shell=True
    )
    match = re.search(r"Parcel\(00000000 00000001", output)
    return match is not None

def wakeup():
    """Wake up device."""
    if not is_screen_on():
        subprocess.check_output(
            "adb shell input keyevent 26",
            shell=True
        )

def unlock(pincode):
    """Unlock device with the given PIN."""
    wakeup()
    comand = (
        "adb shell input keyevent 82"
        " && adb shell input text {}"
        " && adb shell input keyevent 66"
    ).format(pincode)
    subprocess.check_output(
        comand,
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
    if not devices:
        return False
    try:
        result = subprocess.check_output(
            "adb shell getprop sys.boot_completed",
            shell=True).strip()
        return result == "1"
    except subprocess.CalledProcessError:
        return False

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

def connect_adb_through_wifi():
    """Configure `adb` through a wifi connection."""
    net_output = subprocess.check_output(
        "adb shell ip -f inet addr show wlan0",
        shell=True
    )
    ip_address = re.search(r"inet \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", net_output).group()[5:]
    subprocess.check_output(
        "adb tcpip 5555",
        shell=True
    )
    subprocess.check_output(
        "adb connect {}".format(ip_address),
        shell=True
    )

def reconnect_adb_through_usb():
    """Connect adb back to USB while in wifi."""
    try:
        subprocess.check_output(
            "adb reconnect",
            shell=True
        )
    except subprocess.CalledProcessError:
        pass
    