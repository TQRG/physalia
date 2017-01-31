""" Module with main classes for energy profiling
"""

import time
from physalia.power_meters import EmulatedPowerMeter
from physalia.models import Measurement


class AndroidUseCase(object):
    """ Implementation an Android use case

    Attributes:
        power_meter     power meter to use for measurements
        name            name identifier of the use case
        app_pkg         package
        app_version     version of the app
        prepare         method to run before interaction
        interact        method with Android interaction
    """

    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case.

    power_meter = EmulatedPowerMeter()

    def __init__(self, name, app_pkg, app_version, prepare, run):
        self.name = name
        self.app_pkg = app_pkg
        self.app_version = app_version
        self.prepare = prepare
        self._run = run

    def run(self):
        """ Method that tuns the measurements of the routine stored in ```run```
        """
        self.prepare()
        self.power_meter.start()
        self._run()
        energy_consumption, duration = self.power_meter.stop()
        measurement = Measurement(
            time.time(),
            self.name,
            self.app_pkg,
            self.app_version,
            'Nexus5X',  # TODO: get device
            duration,
            energy_consumption,
        )
        measurement.persist()

    def run_experiment(self, count=30):
        """ Runs a batch of experiments
        """
        for _ in range(count):
            self.run()
