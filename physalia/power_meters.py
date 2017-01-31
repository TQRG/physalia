import abc
import time


class PowerMeter(object):
    """Abstract class to implement interaction with a power monitor
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def start(self):
        """Method to start measuring energy consumption
        """
        return

    @abc.abstractmethod
    def stop(self):
        """Method to stop measuring energy consumption

        Returns:
            Energy consumption in Joules
        """
        return


class EmulatedPowerMeter(PowerMeter):
    """PowerMeter implementation to emulate a power monitor
    """

    def __init__(self):
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        duration = time.time() - self.start_time
        energy_consumption = duration
        return energy_consumption, duration
