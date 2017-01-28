import unittest
from physalia.models import Measurement


class TestMeasurement(unittest.TestCase):
    def test_persist(self):
        measurement = Measurement(
            1485634263.096069,
            'login',
            'Nexus5X',
            1000,
            1000,
            2,
            30
        )
        measurement.persist()
