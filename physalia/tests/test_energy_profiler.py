"""Test Energy Profiler module."""

from time import sleep
import subprocess
import unittest
from whichcraft import which
from physalia.energy_profiler import AndroidUseCase, AndroidViewClientUseCase
from physalia.models import Measurement

# pylint: disable=missing-docstring

def check_adb():
    """Check whether adb is available."""
    return which("adb") is not None

def is_android_device_available():
    """Get available android devices."""
    if not check_adb():
        return False
    result = subprocess.check_output("adb devices", shell=True)
    devices = result.partition('\n')[2].replace('\n', '').split('\tdevice')
    devices = [device for device in devices if len(device) > 2]
    return len(devices) > 0


class TestMonitorEnergy(unittest.TestCase):

    TEST_CSV_STORAGE = "./test_energy_profiler_db.csv"

    def setUp(self):
        Measurement.csv_storage = self.TEST_CSV_STORAGE
        self.addCleanup(Measurement.clear_database)

    @unittest.skipUnless(is_android_device_available(),
                         "Android device not found")
    def test_simple(self):

        def prepare(_):
            prepare.count += 1
        prepare.count = 0

        def run(_):
            run.count += 1
        run.count = 0
        use_case = AndroidUseCase(
            "Login",
            None,
            "com.test.app",
            "0.01",
            run,
            prepare
        )
        count = 30
        use_case.profile_and_persist(count)
        self.assertEqual(prepare.count, count)
        self.assertEqual(run.count, count)

        with open(self.TEST_CSV_STORAGE, 'r') as file_desc:
            content = file_desc.read()
            self.assertEqual(len(content.split('\n')), 31)

    @unittest.skipUnless(is_android_device_available(),
                         "Android device not found")
    def test_with_apk(self):
        # pylint: disable=no-self-use

        def prepare(use_case):
            use_case.prepare_apk()

        def run(use_case):
            use_case.open_app()
            sleep(1)

        android_use_case = AndroidUseCase(
            "OpenApp",
            "./fdroid.apk",
            "org.fdroid.fdroid",
            "0.01",
            run,
            prepare
        )
        android_use_case.run()

    @unittest.skipUnless(is_android_device_available(),
                         "Android device not found")
    def test_android_vc_use_case(self):

        def run(use_case):
            use_case.open_app()
            sleep(2)
            use_case.view_client.dump(window=-1)
            self.assertTrue(
                use_case.view_client.findViewWithText(u'''What's New''')
            )

        use_case = AndroidViewClientUseCase(
            "OpenApp",
            "./fdroid.apk",
            "org.fdroid.fdroid",
            "0.01",
            run
        )
        use_case.run()
