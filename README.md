[![Build Status](https://travis-ci.org/TQRG/physalia.svg?branch=master)](https://travis-ci.org/TQRG/physalia)
[![PyPI version](https://badge.fury.io/py/physalia.svg)](https://badge.fury.io/py/physalia)
[![PyPI downloads](https://img.shields.io/pypi/d/physalia.svg)](https://pypi.python.org/pypi/physalia)
[![PyPI status](https://img.shields.io/pypi/status/physalia.svg)](https://pypi.python.org/pypi/physalia)



# Physalia

Energy measurement framework for Mobile Apps.

More info and documentation in the [website](https://tqrg.github.io/physalia/).

## Install

```
$ pip install physalia
```

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
