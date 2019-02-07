from physalia.power_meters import MonsoonPowerMeter
from physalia.energy_profiler import AndroidUseCase
from time import sleep


power_meter = MonsoonHVPMPowerMeter(voltage=3.8, serial=None)

def run(usecase):
	sleep(2) # some work
	
use_case = AndroidUseCase(
  'login',
  'path/to/apk',
  'com.test.app',
  '0.0',
  prepare=None,
  run=run,
  cleanup=None
)
measurement = use_case.run(power_meter=power_meter)
print(measurement)
