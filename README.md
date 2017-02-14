[![Build Status](https://travis-ci.org/TQRG/physalia.svg?branch=master)](https://travis-ci.org/TQRG/physalia)

# Physalia

Energy tests framework for Android

## Example

````
from physalia.energy_profiler import AndroidUseCase

def prepare():
	pass
def run():
	pass
	
use_case = AndroidUseCase('login', 'com.test.app', '12', run, prepare)
use_case.profile()
````
