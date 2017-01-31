# Physalia

Energy tests framework for Android

## Example

````
from physalia.energy_profiler import AndroidUseCase

def prepare():
	pass
def run():
	pass
	
use_case = AndroidUseCase('login', 'com.test.app', '12', prepare, run)
use_case.run_experiment()
````