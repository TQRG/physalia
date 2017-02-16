""" Test Models module
"""

import unittest
from mock import patch, MagicMock
import numpy
from physalia.models import Measurement
from physalia.utils import GREEK_ALPHABET

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

def create_random_samples(count=30, seed=1):
    numpy.random.seed(seed)
    energy_consumptions_a = numpy.random.normal(loc=10.0,
                                                scale=1.0,
                                                size=count)
    sample_a = [
        create_measurement(
            energy_consumption=energy_consumptions_a[i]
        )
        for i in range(count)
    ]
    energy_consumptions_b = numpy.random.normal(loc=12.0,
                                                scale=1.0,
                                                size=count)
    sample_b = [
        create_measurement(
            energy_consumption=energy_consumptions_b[i]
        )
        for i in range(count)
    ]
    return sample_a, sample_b

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

    def test_hypothesis_test(self):
        sample_a, sample_b = create_random_samples()
        _, pvalue = Measurement.hypothesis_test(sample_a, sample_b)
        self.assertLess(pvalue, 0.05)

    def test_fancy_hypothesis_test(self):
        from StringIO import StringIO
        from string import Template

        # sample_a, sample_b = create_random_samples()
        with patch('physalia.models.Measurement.hypothesis_test',
                   MagicMock(return_value=(0, 0.0001))):
            out = StringIO()
            Measurement.fancy_hypothesis_test(
                None, None,
                "login with email",
                "login with facebook",
                out=out
            )
            output = out.getvalue()

            self.assertEqual(
                output,
                Template(
                    "Hypothesis testing:\n"
                    "\t$H0: $mu login with email = $mu login with facebook.\n"
                    "\t$H1: $mu login with email $neq $mu login with facebook.\n"
                    "\n"
                    "Applying Welch's t-test with $alpha=0.05, the null"
                    " hypothesis is rejected (p-value=<0.001).\n"
                    "Thus, one can say that the means of populations"
                    " \"login with email\" and \"login with facebook\" are"
                    " different.\n"
                ).substitute(GREEK_ALPHABET)
            )
        with patch('physalia.models.Measurement.hypothesis_test',
                   MagicMock(return_value=(0, 0.061231))):
            out = StringIO()
            Measurement.fancy_hypothesis_test(
                None, None,
                "login with email",
                "login with facebook",
                out=out
            )
            output = out.getvalue()

            self.assertEqual(
                output,
                Template(
                    "Hypothesis testing:\n"
                    "\t$H0: $mu login with email = $mu login with facebook.\n"
                    "\t$H1: $mu login with email $neq $mu login with facebook.\n"
                    "\n"
                    "Applying Welch's t-test with $alpha=0.05, the null"
                    " hypothesis is not rejected (p-value=0.061).\n"
                    "Thus, it was not possible to find evidence that"
                    " the means of populations login with email and "
                    "login with facebook are different.\n"
                ).substitute(GREEK_ALPHABET)
            )
