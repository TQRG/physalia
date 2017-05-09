"""Test energy_profiler module."""

import unittest

from physalia.energy_profiler import AndroidUseCase

# pylint: disable=missing-docstring

class TestEnergyProfiler(unittest.TestCase):

    def test_empty_android_use_case(self):
        # pylint: disable=no-self-use
        use_case = AndroidUseCase(
            name="Test",
            app_apk="no/path",
            app_pkg="no.package",
            app_version="0.0.0",
            run=None,
            prepare=None,
            cleanup=None
        )
        use_case.run()
