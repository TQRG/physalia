[![Build Status](https://travis-ci.org/TQRG/physalia.svg?branch=master)](https://travis-ci.org/TQRG/physalia)
[![PyPI version](https://badge.fury.io/py/physalia.svg)](https://badge.fury.io/py/physalia)
[![PyPI downloads](https://img.shields.io/pypi/d/physalia.svg)](https://pypi.python.org/pypi/physalia)
[![PyPI status](https://img.shields.io/pypi/status/physalia.svg)](https://pypi.python.org/pypi/physalia)
[![Code Health](https://landscape.io/github/TQRG/physalia/master/landscape.svg?style=flat)](https://landscape.io/github/TQRG/physalia/master)


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

## Contributing

Please help us improve this library!

If you have ideas for new features or anything behaves unexpectedly please report an issue.

If you find an issue you can actually help fixing please make a pull request of your code.

### Running tests

To run all tests and checks locally run:

`$ detox -e py27,py36`
