""" Module with main classes for energy profiling
"""

import time
import subprocess
import types
import click
from physalia.power_meters import EmulatedPowerMeter
from physalia.models import Measurement


class AndroidUseCase(object):
    """ Implementation of an Android use case

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

    def __init__(self, name, app_apk, app_pkg, app_version, prepare, run):
        self.name = name
        self.app_apk = app_apk
        self.app_pkg = app_pkg
        self.app_version = app_version
        self.prepare = types.MethodType(prepare, self)
        self._run = types.MethodType(run, self)

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

    def prepare_apk(self):
        click.secho("Uninstalling {}".format(self.app_pkg), fg='blue')
        subprocess.check_output(["adb", "uninstall", self.app_pkg])
        click.secho("Installing {}".format(self.app_apk), fg='blue')
        subprocess.check_output(["adb", "install", self.app_apk])

    def open_app(self):
        click.secho("Opening app {}".format(self.app_pkg), fg='blue')
        subprocess.check_output(
            "adb shell monkey -p {} --pct-syskeys 0 1".format(self.app_pkg),
            shell=True
        )
