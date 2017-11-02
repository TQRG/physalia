"""Models to interact with different power meters."""

import abc
import time
import warnings

import click
from Monsoon import Operations as operations
from Monsoon.sampleEngine import SampleEngine
from Monsoon import LVPM

from physalia.third_party import monsoon_async
from physalia.utils import android
from physalia.utils.monsoon import set_voltage_if_different


class PowerMeter(object):
    """Abstract class for interaction with a power monitor."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def start(self):
        """Start measuring energy consumption."""
        return

    @abc.abstractmethod
    def stop(self):
        """Stop measuring energy consumption.

        Returns:
            tuple: energy consumption in Joules; duration; error flag.

        """
        return

    def reinit(self):
        """Reinitialize power meter upon unexpected behavior."""
        pass


class EmulatedPowerMeter(PowerMeter):
    """PowerMeter implementation to emulate a power monitor."""

    def __init__(self):  # noqa: D102,D107
        self.start_time = None

    def start(self):
        """Start measuring energy consumption."""
        self.start_time = time.time()

    def stop(self):
        """Stop measuring energy consumption.

        Returns:
            tuple: energy consumption in Joules; duration; error flag.

        """
        duration = time.time() - self.start_time
        energy_consumption = duration
        return energy_consumption, duration, False

    def __str__(self):
        """Return the name of this power meter."""
        return "Emulated"

class MonsoonPowerMeter(PowerMeter):
    """PowerMeter implementation for Monsoon.

    Make sure the Android device has Passlock disabled.
    Your server and device have to be connected to the same network.
    """

    def __init__(self, voltage=3.8, serial=None):  # noqa: D102,D107
        self.monsoon = None
        self.serial = serial
        self.voltage = voltage
        self.monsoon_reader = None
        self.monsoon_data = None
        self.engine = None
        self.setup_monsoon()

        click.secho(
            "Monsoon is ready.",
            fg='green'
        )
        if not android.is_android_device_available():
            click.secho(
                "You can now turn the phone on.",
                fg='blue'
            )
        for i in range(180):
            time.sleep(1)
            if android.is_android_device_available():
                time.sleep(2)
                click.secho(
                    "Found a {}!".format(android.get_device_model()),
                    fg='green'
                )
                break
            if i%15 == 0:
                click.secho(
                    "Waiting for an Android device...",
                    fg='blue'
                )
            if i == 180:
                raise Exception("Could not find device.")
        android.connect_adb_through_wifi()
        self.monsoon_usb_enabled(False)
        if android.is_locked():
            click.secho(
                "Device seems to be locked. "
                "Disabling Passlock is recommended!",
                fg='yellow'
            )

    def reinit(self):
        """Reinitialize power meter upon unexpected behavior."""
        warnings.warn(
            "reinit is deprecated and does nothing",
            DeprecationWarning
        )

    def setup_monsoon(self):
        """Set up monsoon.

        Args:
            voltage: Voltage output of the power monitor.
            serial: serial number of the power monitor.
        """
        click.secho(
            "Setting up Monsoon {} with {}V...".format(
                self.serial, self.voltage
            ),
            fg='blue'
        )
        self.monsoon = LVPM.Monsoon()
        self.monsoon.setup_usb(self.serial)
        set_voltage_if_different(self.monsoon, self.voltage)
        self.engine = SampleEngine(self.monsoon)
        self.engine.ConsoleOutput(False)

        if android.is_android_device_available():
            android.reconnect_adb_through_usb()
        self.monsoon_usb_enabled(True)

    def monsoon_usb_enabled(self, enabled):
        """Enable/disable monsoon's usb port."""
        # pylint: disable=too-many-function-args
        # something is conflicting with timeout_decorator
        self.monsoon.setUSBPassthroughMode(
            {
                True:operations.USB_Passthrough.On,
                False:operations.USB_Passthrough.Off,
            }[enabled]
        )

    def start(self):
        """Start measuring energy consumption."""
        self.monsoon_reader = monsoon_async.MonsoonReader(
            self.engine,
        )
        self.monsoon_reader.start()

    def stop(self):
        """Stop measuring."""
        self.monsoon_reader.stop()
        samples = self.engine.getSamples()
        if len(samples) == 3:
            timestamps = samples[0]
            currents = samples[1]
            if timestamps:
                sample_hz = 50000
                delta_time = 1/sample_hz
                energy_consumption = sum(currents)*delta_time
                duration = timestamps[-1]
                return energy_consumption, duration, False
        return None, None, True

    def __str__(self):
        """Return the name of this power meter."""
        return "Monsoon"
