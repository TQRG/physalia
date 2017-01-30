import unittest
from physalia.energy_profiler import monitor_energy


class TestMonitorEnergy(unittest.TestCase):
    def test_key(self):
        @monitor_energy
        def useless_func():
            var = 0
            for i in range(1000):
                var = var + i
        useless_func()
