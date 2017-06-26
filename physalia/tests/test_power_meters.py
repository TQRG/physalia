"""Test power_meters module."""

import time
import unittest

from physalia.power_meters import MonsoonPowerMeter
from physalia.utils.monsoon import is_monsoon_available

# pylint: disable=missing-docstring

class TestPowerMeters(unittest.TestCase):

    @unittest.skipUnless(is_monsoon_available(),
                         "Monsoon is required to run this test.")
    def test_collect_sample(self):
        desired_duration = 2
        power_meter = MonsoonPowerMeter(voltage=3.8, serial=12886)
        power_meter.start()
        time.sleep(desired_duration)
        energy_consumption, duration, error = power_meter.stop()
        self.assertFalse(error, "Power meter flagged an error.")
        self.assertAlmostEqual(duration, desired_duration, delta=1)
        self.assertGreater(energy_consumption, 0)

    @unittest.skipUnless(is_monsoon_available(),
                         "Monsoon is required to run this test.")
    def test_collect_tiny_sample(self):
        """Test measurements with less than a second.

        There was originally an error in which samples with less than 1
        second would not return any measurements.
        Still, such short measurements are not recommended.
        The first 0.2 seconds are not returning any data.
        """

        desired_duration = 0.3
        power_meter = MonsoonPowerMeter(voltage=3.8, serial=12886)
        power_meter.start()
        time.sleep(desired_duration)
        energy_consumption, _, error = power_meter.stop()
        self.assertFalse(error, "Power meter flagged an error.")
        self.assertGreater(energy_consumption, 0)
        