"""Test Assert module."""

import unittest
from physalia import asserts
from physalia.fixtures.models import create_random_sample

# pylint: disable=missing-docstring

class TestAssert(unittest.TestCase):

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
