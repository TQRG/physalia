""" Test Energy Profiler module
"""

from time import sleep
import unittest
from physalia.energy_profiler import AndroidUseCase, AndroidViewClientUseCase
from physalia.models import Measurement

# pylint: disable=missing-docstring


class TestMonitorEnergy(unittest.TestCase):

    TEST_CSV_STORAGE = "./test_energy_profiler_db.csv"

    def setUp(self):
        Measurement.csv_storage = self.TEST_CSV_STORAGE
        self.addCleanup(Measurement.clear_database)

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
        # pylint: disable=no-self-use

        def prepare(use_case):
            use_case.prepare_apk()

        def run(use_case):
            use_case.open_app()
            sleep(1)

        use_case = AndroidUseCase(
            "OpenApp",
            "./fdroid.apk",
            "org.fdroid.fdroid",
            "0.01",
            prepare,
            run
        )
        use_case.run()

    def test_android_vc_use_case(self):

        def prepare(_):
            pass

        def run(use_case):
            use_case.open_app()
            sleep(1)
            use_case.view_client.dump(window=-1)
            self.assertTrue(
                use_case.view_client.findViewWithText(u'''What's New''')
            )

        use_case = AndroidViewClientUseCase(
            "OpenApp",
            "./fdroid.apk",
            "org.fdroid.fdroid",
            "0.01",
            prepare,
            run
        )
        use_case.run()
