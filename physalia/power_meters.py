"""Models to interact with different power meters."""

import abc
import time
from threading import Thread
from physalia.third_party.monsoon import Monsoon


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
    """PowerMeter implementation for Monsoon."""

    def __init__(self, serial=12886):  # noqa: D102
        self.serial = serial
        self.monsoon = None
        self.thread = None
        self.monsoon_data = None

    def start(self):
        """Start measuring energy consumption."""
        def start_method():
            """Start measuring in different thread."""
            self.monsoon = Monsoon(serial=self.serial)
            self.monsoon_data = self.monsoon.take_samples(
                sample_hz=200, sample_num=200,
                sample_offset=0, live=False
            )

        self.thread = Thread(target=start_method)
        self.thread.start()

    def stop(self):
        """Stop measuring."""
        self.thread.join()
        energy_consumption = sum(self.monsoon_data.data_points)/self.monsoon_data.hz
        duration = len(self.monsoon_data.data_points)/self.monsoon_data.hz
        return energy_consumption, duration
