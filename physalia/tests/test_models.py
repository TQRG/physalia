import unittest
from physalia.models import Measurement


class TestMeasurement(unittest.TestCase):
    TEST_CSV_STORAGE = "./test_db.csv"

    def test_persist(self):
        Measurement.csv_storage = self.TEST_CSV_STORAGE
        self.addCleanup(Measurement.clear_database)
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
        with open(self.TEST_CSV_STORAGE, 'r') as file_desc:
            content = file_desc.read()
        self.assertTrue(
            """1485634263.096069,login,Nexus5X,1000,1000,2,30""" in content)
