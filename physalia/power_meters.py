"""Models to interact with different power meters."""

import abc
import time
from threading import Thread
import click
from physalia.third_party.monsoon import Monsoon
from physalia.utils import android


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
            Energy consumption in Joules

        """
        return


class EmulatedPowerMeter(PowerMeter):
    """PowerMeter implementation to emulate a power monitor."""

    def __init__(self):  # noqa: D102
        self.start_time = None

    def start(self):
        """Start measuring energy consumption."""
        self.start_time = time.time()

    def stop(self):
        """Stop measuring energy consumption.

        Returns:
            Energy consumption in Joules

        """
        duration = time.time() - self.start_time
        energy_consumption = duration
        return energy_consumption, duration

class MonsoonPowerMeter(PowerMeter):
    """PowerMeter implementation for Monsoon.
        
        Make sure the Android device has Passlock disabled.
        Your server and device have to be connected to the same network.
    """

    def __init__(self, voltage=3.8, hz=50000, serial=12886):  # noqa: D102
        self.monsoon = None
        self.thread = None
        self.monsoon_data = None
        self.voltage = None
        self.serial = None
        self.hz = hz

        self.setup_monsoon(voltage, serial)
        click.secho(
            "Monsoon is ready.",
            fg='green'
        )
        for i in range(50):
            click.secho(
                "Waiting for an Android device.",
                fg='green'
            )
            if android.is_android_device_available():
                break
            time.sleep(3)
        android.connect_adb_through_wifi()
        self.monsoon.usb(self.monsoon, 'off')
        android.wakeup()

    def setup_monsoon(self, voltage, serial):
        """Setup monsoon.
        
        Args:
            voltage: Voltage output of the power monitor.
            serial: serial number of the power monitor.
        """
        click.secho(
            "Setting up Monsoon {} with {}V...".format(
                serial, voltage
            ),
            fg='green'
        )
        
        self.serial = serial
        self.voltage = voltage
        self.monsoon = Monsoon(serial=self.serial)
        self.monsoon.set_voltage(self.voltage)
        self.monsoon.usb(self.monsoon, 'on')

    def start(self):
        """Start measuring energy consumption."""
        def start_method():
            """Start measuring in different thread."""
            self.monsoon = Monsoon(serial=self.serial)
            self.monsoon.set_voltage(self.voltage)
            self.monsoon_data = self.monsoon.take_samples(
                sample_hz=self.hz, sample_num=500000,
                sample_offset=0, live=False
            )

        self.thread = Thread(target=start_method)
        self.thread.start()

    def stop(self):
        """Stop measuring."""
        self.thread.join()
        energy_consumption = sum(self.monsoon_data.data_points)/self.monsoon_data.hz/1000
        duration = len(self.monsoon_data.data_points)/self.monsoon_data.hz
        return energy_consumption, duration
