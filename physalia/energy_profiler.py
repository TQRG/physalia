""" Module with main classes for energy profiling
"""

import time
import subprocess
import types
import sys
import click
from com.dtmilano.android.viewclient import ViewClient
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
    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    power_meter = EmulatedPowerMeter()

    def __init__(self, name, app_apk, app_pkg, app_version,
                 run, prepare=None, cleanup=None):
        self.name = name
        self.app_apk = app_apk
        self.app_pkg = app_pkg
        self.app_version = app_version
        self._run = types.MethodType(run, self)
        if prepare:
            self._prepare = types.MethodType(prepare, self)
        if cleanup:
            self._cleanup = types.MethodType(cleanup, self)

    def _prepare(self):
        # pylint: disable=method-hidden
        pass

    def _cleanup(self):
        # pylint: disable=method-hidden
        pass

    def prepare(self):
        """ Method that prepares environment for running
        """
        self._prepare()

    def cleanup(self):
        """ Method that cleans environment after running
        """

    def run(self):
        """ Method that tuns the measurements of the routine stored in ```run```
        """
        self.prepare()
        self.power_meter.start()
        self._run()
        energy_consumption, duration = self.power_meter.stop()
        return Measurement(
            time.time(),
            self.name,
            self.app_pkg,
            self.app_version,
            self.get_device_model(),
            duration,
            energy_consumption,
        )

    def profile(self, verbose=True, count=30):
        """ Runs a batch of measurements
        """
        results = [self.run() for _ in range(count)]
        if verbose:
            click.secho("Energy consumption results for {}: "
                        "{:.3f} Joules (s = {:.3f}).\n"
                        "It took {:.1f} seconds (s = {:.1f})."
                        .format(self.app_pkg, *Measurement.describe(results)),
                        fg='green')
        return results

    def profile_and_persist(self, verbose=True, count=30):
        """ Measures a batch of measurements and save it for
        later comparison
        """
        for measurement in self.profile(verbose, count):
            measurement.persist()

    def get_device_model(self, serialno=None):
        """ Finds out which is the current connected device model
        """
        # pylint: disable=no-self-use

        if serialno:
            command = ("adb shell -s {} "
                       "getprop ro.product.model").format(serialno)
        else:
            command = "adb shell getprop ro.product.model"
        model = subprocess.check_output(
            command,
            shell=True
        ).strip()
        return model

    def prepare_apk(self):
        """Reinstalls app in the Android device
        """
        click.secho("Uninstalling {}".format(self.app_pkg), fg='blue')
        subprocess.check_output(["adb", "uninstall", self.app_pkg])
        click.secho("Installing {}".format(self.app_apk), fg='blue')
        subprocess.check_output(["adb", "install", self.app_apk])

    def open_app(self):
        """Opens app in the device
        """
        click.secho("Opening app {}".format(self.app_pkg), fg='blue')
        subprocess.check_output(
            "adb shell monkey -p {} --pct-syskeys 0 1".format(self.app_pkg),
            shell=True
        )

    def kill_app(self):
        """Kills the app of this use case
        """
        click.secho("Killing app {}".format(self.app_pkg), fg='blue')
        subprocess.check_output(
            "adb shell am force-stop {}".format(self.app_pkg),
            shell=True
        )
    


class AndroidViewClientUseCase(AndroidUseCase):
    """ Implementation of an Android use case
    that uses Android view client
    """

    def get_device_model(self, serialno=None):
        """ Finds out which is the current connected device model.
        It uses the serialno if a device is already connected
        using AndroidviewClient
        """
        if serialno is None:
            serialno = self.serialno
        super(AndroidViewClientUseCase, self).get_device_model(serialno)

    def start_view_client(self):
        """ Setups AndroidViewClient
        """
        # pylint: disable=attribute-defined-outside-init

        original_argv = sys.argv
        sys.argv = original_argv[:1]
        kwargs1 = {'ignoreversioncheck': False,
                   'verbose': False,
                   'ignoresecuredevice': False}
        device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
        kwargs2 = {'forceviewserveruse': False,
                   'useuiautomatorhelper': False,
                   'ignoreuiautomatorkilled': True,
                   'autodump': False,
                   'startviewserver': True,
                   'compresseddump': True}
        view_client = ViewClient(device, serialno, **kwargs2)
        sys.argv = original_argv
        self.device = device
        self.serialno = serialno
        self.view_client = view_client

    def prepare(self):
        """ Method that preparation environment for running.
        It setups Android View Client.
        """
        self.start_view_client()
        self._prepare()
        time.sleep(1)
        self.refresh()

    def refresh(self):
        while True:
            try:
                self.view_client.dump(window='-1')
            except RuntimeError:
                continue
            break
