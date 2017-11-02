""" Test Models module
"""

import unittest
from physalia.models import Measurement
from physalia.fixtures.models import create_measurement
from physalia.fixtures.models import create_random_sample

# pylint: disable=missing-docstring

class TestMeasurement(unittest.TestCase):
    TEST_CSV_STORAGE = "./test_models_db.csv"

    def setUp(self):
        Measurement.csv_storage = self.TEST_CSV_STORAGE
        self.addCleanup(Measurement.clear_database)

    def test_persist(self):
        measurement = create_measurement()
        measurement.persist()
        with open(self.TEST_CSV_STORAGE, 'r') as file_desc:
            content = file_desc.read()
        self.assertIn(
            """1485634263.096069,login,com.package,1.0.0,Nexus 5X,2.0,30.0,NA,True""",
            content
        )

    def test_get_unique_apps(self):
        for _ in range(10):
            measurement = create_measurement(app_pkg="com.test.one")
            measurement.persist()
            measurement = create_measurement(app_pkg="com.test.two")
            measurement.persist()
            measurement = create_measurement(app_pkg="com.test.three")
            measurement.persist()
        self.assertEqual(
            set(Measurement.get_unique_apps()),
            {"com.test.one", "com.test.two", "com.test.three"}
        )

    def test_get_unique_use_cases(self):
        measurements = []
        for _ in range(10):
            measurements.append(create_measurement(use_case="one"))
            measurements.append(create_measurement(use_case="two"))
            measurements.append(create_measurement(use_case="three"))
        self.assertEqual(
            Measurement.get_unique_use_cases(measurements),
            {"one", "two", "three"}
        )

    def test_describe_app_use_case(self):
        for i in range(10):
            measurement = create_measurement(
                use_case="login",
                duration=i,
                energy_consumption=i * 2
            )
            measurement.persist()
        real_stats = Measurement.describe_app_use_case(
            measurement.app_pkg,
            measurement.use_case
        )
        expected_stats = (9, 5.745, 4.5, 2.872)
        # pairwise assertion:
        for (first, second) in zip(real_stats, expected_stats):
            self.assertAlmostEqual(first, second, places=3)


    def test_get_energy_ranking(self):
        sample = (
            create_random_sample(10, 1, app_pkg="com.app1") +
            create_random_sample(11, 1, app_pkg="com.app2") +
            create_random_sample(12, 1, app_pkg="com.app3") +
            create_random_sample(13, 1, app_pkg="com.app4") +
            create_random_sample(14, 1, app_pkg="com.app5") +
            create_random_sample(15, 1, app_pkg="com.app6")
        )
        for measurement in sample:
            measurement.persist()
        ranking = Measurement.get_energy_ranking()
        self.assertEqual(
            list(ranking.keys()),
            [
                "com.app1",
                "com.app2",
                "com.app3",
                "com.app4",
                "com.app5",
                "com.app6",
            ]
        )
        compare_sample = create_random_sample(12.5, 0.5, app_pkg="com.app7")
        self.assertEqual(
            Measurement.get_position_in_ranking(compare_sample),
            (4, 6)
        )
