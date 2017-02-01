import sys
from time import sleep
import unittest
from com.dtmilano.android.viewclient import ViewClient
from physalia.energy_profiler import AndroidUseCase
from physalia.models import Measurement


class TestMonitorEnergy(unittest.TestCase):

    TEST_CSV_STORAGE = "./test_db.csv"

    def test_simple(self):
        Measurement.csv_storage = self.TEST_CSV_STORAGE
        self.addCleanup(Measurement.clear_database)

        def prepare(use_case):
            prepare.count += 1
        prepare.count = 0

        def run(use_case):
            run.count += 1
        run.count = 0
        use_case = AndroidUseCase(
            "Login",
            None,
            "com.test.app",
            "0.01",
            prepare,
            run
        )
        count = 30
        use_case.run_experiment(count)
        self.assertEqual(prepare.count, count)
        self.assertEqual(run.count, count)

        with open(self.TEST_CSV_STORAGE, 'r') as file_desc:
            content = file_desc.read()
            self.assertEqual(len(content.split('\n')), 31)

    def test_with_apk(self):
        Measurement.csv_storage = self.TEST_CSV_STORAGE
        self.addCleanup(Measurement.clear_database)

        def connect_device():
            original_argv = sys.argv
            sys.argv = original_argv[:1]
            kwargs1 = {'ignoreversioncheck': False, 'verbose': False, 'ignoresecuredevice': False}
            device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
            kwargs2 = {'forceviewserveruse': False, 'useuiautomatorhelper': False, 'ignoreuiautomatorkilled': True, 'autodump': False, 'startviewserver': True, 'compresseddump': True}
            vc = ViewClient(device, serialno, **kwargs2)
            sys.argv = original_argv
            return device, serialno, vc

        def prepare(use_case):
            use_case.prepare_apk()
            device, serialno, vc = connect_device()

        def run(use_case):
            use_case.open_app()
            sleep(1)
            pass

        use_case = AndroidUseCase(
            "Login",
            "./fdroid.apk",
            "org.fdroid.fdroid",
            "0.01",
            prepare,
            run
        )
        use_case.run()
