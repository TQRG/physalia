import time
from physalia.power_meters.power_meter import PowerMeter


class EmulatedPowerMeter(PowerMeter):
    """PowerMeter implementation to emulate a power monitor
    """
    def start(self):
        self.start_time = time.time()

    def stop(self):
        return time.time() - self.start_time
