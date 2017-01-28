import unittest
from physalia.energy_profiler import monitor_energy


class TestMonitorEnergy(unittest.TestCase):
    def test_key(self):
        @monitor_energy
        def useless_func():
            for i in range(1000):
                i + i
        useless_func()
