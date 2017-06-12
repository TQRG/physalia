"""Module with main classes for energy profiling."""

import time
import subprocess
import types
import click
from physalia.power_meters import EmulatedPowerMeter
from physalia.models import Measurement
import physalia.utils.android as android_utils
from physalia.exceptions import PhysaliaExecutionFailed


class AndroidUseCase(object):
    """Implementation of an Android use case.

    Attributes:
        power_meter     power meter to use for measurements
        name            name identifier of the use case
        app_pkg         package
        app_version     version of the app
        prepare         method to run before interaction
        interact        method with Android interaction

    """

    # pylint: disable=not-callable
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    default_power_meter = EmulatedPowerMeter()

    def __init__(self, name, app_apk, app_pkg, app_version,
                 run=None, prepare=None, cleanup=None):  # noqa: D102
        self.name = name
        self.app_apk = app_apk
        self.app_pkg = app_pkg
        self.app_version = app_version
        self.power_meter = None
        if run:
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

    def _run(self):
        # pylint: disable=method-hidden
        pass

    def prepare(self):
        """Prepare environment for running."""
        self._prepare()

    def cleanup(self):
        """Clean environment after running."""
        self._cleanup()

    def run(self, power_meter=default_power_meter, retry_limit=1):
        """Measure the routine stored in `_run`.

        Returns:
            Measurement: data collected from experiment

        """
        try:
            self.prepare()
            power_meter.start()
            self._run()
            energy_consumption, duration, error_flag = power_meter.stop()
            self.cleanup()
            if error_flag:
                raise PhysaliaExecutionFailed()
            return Measurement(
                time.time(),
                self.name,
                self.app_pkg,
                self.app_version,
                android_utils.get_device_model(),
                duration,
                energy_consumption,
                str(power_meter)
            )
        except KeyboardInterrupt as error:
            raise error
        except BaseException as error:
            click.secho(error.message, fg='red')
            if retry_limit > 0:
                click.secho("Measurement has failed: retrying...", fg='yellow')
                return self.run(power_meter, retry_limit-1)
            raise error

    def profile(self, power_meter=default_power_meter,
                verbose=True, count=30, retry_limit=1,
                save_to_csv=None):
        """Run a batch of measurements.

        Args:
            power_meter     Power meter to use in measurements.
            verbose         Log activiy (default=True).
            count           Run experiment several times (default=30).
            retry_limit     Number of times to retry on error.
            save_to_csv     File name to store mesasurement.
        Returns: Set of measurements

        """
        results = []
        for i in range(count):
            result = self.run(power_meter=power_meter, retry_limit=retry_limit)
            if result:
                results.append(result)
                if save_to_csv:
                    result.save_to_csv(save_to_csv)
            else:
                click.secho("Error in execution {} of {}. Skipping.".format(i, self.name), fg="red")
        if verbose and results:
            click.secho("Energy consumption results for {}: "
                        "{:.3f} Joules (s = {:.3f}).\n"
                        "It took {:.1f} seconds (s = {:.1f})."
                        .format(self.app_pkg, *Measurement.describe(results)),
                        fg='green')
        return results

    def profile_and_persist(self, power_meter=default_power_meter,
                            verbose=True, count=30):
        """Measure a batch of measurements and save it."""
        results = self.profile(power_meter, verbose, count)
        for measurement in results:
            measurement.persist()
        return results

    def uninstall_app(self):
        """Uninstall app of the Android device."""
        click.secho("Uninstalling {}".format(self.app_pkg), fg='blue')
        subprocess.check_output(["adb", "uninstall", self.app_pkg])

    def install_app(self):
        """Install App."""
        click.secho("Installing {}".format(self.app_apk), fg='blue')
        android_utils.install_apk(self.app_apk)

    def prepare_apk(self):
        """Reinstall app in the Android device."""
        self.uninstall_app()
        self.install_app()

    def open_app(self):
        """Open app in the device."""
        click.secho("Opening app {}".format(self.app_pkg), fg='blue')
        subprocess.check_output(
            "adb shell monkey -p {} --pct-syskeys 0 1".format(self.app_pkg),
            shell=True
        )

    def kill_app(self):
        """Tell the device to kill the app of this use case."""
        click.secho("Killing app {}".format(self.app_pkg), fg='blue')
        subprocess.check_output(
            "adb shell am force-stop {}".format(self.app_pkg),
            shell=True
        )
