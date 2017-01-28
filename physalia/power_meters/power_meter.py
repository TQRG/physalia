import abc


class PowerMeter(object):
    """Abstract class to implement interaction with a power monitor
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def start(self):
        """Method to start measuring energy consumption
        """
        return

    def stop(self):
        """Method to stop measuring energy consumption

        Returns:
            Energy consumption in Joules
        """
        return
