"""Example that measures energy consumption of a mobile device for 5 secs."""

# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# reason: this is a very basic usage example

import time
from physalia.power_meters import MonsoonPowerMeter
from physalia.energy_profiler import AndroidUseCase

power_meter = MonsoonPowerMeter(voltage=3.8, serial=12886)

def run(_):
    time.sleep(5)
use_case = AndroidUseCase('physalia-simple-tutorial', None, 'na', 'na', run=run)

measurement = use_case.run(power_meter=power_meter)
print(measurement)
