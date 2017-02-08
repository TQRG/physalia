"""Models to interact with different power meters."""

import abc
import time


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
