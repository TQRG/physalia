"""Test Assert module."""

import unittest
from physalia import asserts
from physalia.fixtures.models import create_random_sample
from physalia.models import Measurement

# pylint: disable=missing-docstring

class TestAssert(unittest.TestCase):
    TEST_CSV_STORAGE = "./test_asserts_db.csv"

    def setUp(self):
        Measurement.csv_storage = self.TEST_CSV_STORAGE
        self.addCleanup(Measurement.clear_database)

    def test_consumption_below(self):
        sample = create_random_sample(10, 1)
        asserts.consumption_below(sample, 11)
        with self.assertRaises(Exception):
            asserts.consumption_below(sample, 9)

    def test_consumption_lower_than_app(self):
        sample_low_energy = create_random_sample(
            9, 1,
            app_pkg='com.sample',
            use_case='login'
        )
        sample_high_energy = create_random_sample(
            12, 1,
            app_pkg='com.sample',
            use_case='login'
        )
        existing_sample_one = create_random_sample(
            10, 1,
            app_pkg='com.persisted',
            use_case='login'
        )
        existing_sample_two = create_random_sample(
            11, 1,
            app_pkg='com.persisted',
            use_case='logout'
        )

        for measurement in existing_sample_one+existing_sample_two:
            measurement.persist()

        asserts.consumption_lower_than_app(
            sample_low_energy, "com.persisted"
        )
        asserts.consumption_lower_than_app(
            sample_low_energy, "com.persisted", "login"
        )
        with self.assertRaises(Exception):
            asserts.consumption_lower_than_app(
                sample_high_energy, "com.persisted"
            )
        with self.assertRaises(Exception):
            asserts.consumption_lower_than_app(
                sample_high_energy, "com.persisted", "login"
            )

    def test_top_percentile(self):
        sample = create_random_sample(
            11, 1,
            app_pkg='com.sample',
            use_case='login'
        )
        for i in range(100):
            existing_sample = create_random_sample(
                i, 1,
                app_pkg=('com.persisted.{}'.format(i)),
                use_case='login'
            )
            for measurement in existing_sample:
                measurement.persist()
        asserts.top_percentile(sample, 12)
        with self.assertRaises(Exception):
            asserts.top_percentile(sample, 11)
