"""Test power_meters module."""

import time
import unittest

import Monsoon.LVPM as LVPM

from physalia.utils.monsoon import is_monsoon_available, get_voltage

# pylint: disable=missing-docstring

class TestMonsoonUtils(unittest.TestCase):

    @unittest.skipUnless(is_monsoon_available(),
                         "Monsoon is required to run this test.")
    def test_get_voltage(self):
        voltage = 4.0
        monsoon = LVPM.Monsoon()
        monsoon.setup_usb()
        monsoon.setVout(voltage)
        self.assertEqual(voltage, get_voltage(monsoon))
