""" Test Models module
"""

import unittest
from physalia.models import Measurement

# pylint: disable=missing-docstring


def create_measurement(use_case='login',
                       app_pkg='com.package',
                       duration=2,
                       energy_consumption=30):
    """Fake data for measurement"""
    return Measurement(
        1485634263.096069,  # timestamp
        use_case,           # use_case
        app_pkg,            # application package
        '1.0.0',            # version
        'Nexus 5X',         # device model
        duration,           # duration
        energy_consumption  # energy consumption
    )


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
        self.assertTrue(
            """1485634263.096069,login,com.package,1.0.0,Nexus 5X,2,30"""
            in content
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
        for _ in range(10):
            measurement = create_measurement(use_case="one")
            measurement.persist()
            measurement = create_measurement(use_case="two")
            measurement.persist()
            measurement = create_measurement(use_case="three")
            measurement.persist()
        self.assertEqual(
            set(Measurement.get_unique_use_cases()),
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
