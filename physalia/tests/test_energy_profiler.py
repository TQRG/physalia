import unittest
from physalia.energy_profiler import AndroidUseCase
from physalia.models import Measurement


class TestMonitorEnergy(unittest.TestCase):

    TEST_CSV_STORAGE = "./test2_db.csv"

    def test_key(self):
        Measurement.csv_storage = self.TEST_CSV_STORAGE
        self.addCleanup(Measurement.clear_database)

        def prepare():
            prepare.count += 1
        prepare.count = 0

        def run():
            run.count += 1
        run.count = 0
        use_case = AndroidUseCase(
            "Login",
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
