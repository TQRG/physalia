"""Models that require persistence
"""

import csv
import os


class Measurement(object):
    """Class for with energy measurement information

    Attributes:
        timestamp               When the execution started.
        use_case                Key identifier of the use case.
        device_model            Device where the measurements were performed.
        duration                Time it takes to execute the use case.
        energy_consumption_mean Mean of the measurements.
        energy_consumption_std  Standard deviation of the measurements.
        energy_consumption_n    Sample size of measurements.
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    csv_storage = "./db.csv"

    def __init__(
            self,
            timestamp,
            use_case,
            app_pkg,
            app_version,
            device_model,
            duration,
            energy_consumption
    ):
        self.persisted = False
        self.timestamp = timestamp
        self.use_case = use_case
        self.app_pkg = app_pkg
        self.app_version = app_version
        self.device_model = device_model
        self.duration = duration
        self.energy_consumption = energy_consumption

    def persist(self):
        """ Store measurement in the database."""
        if self.persisted:
            return False
        else:
            with open(self.csv_storage, 'a') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([
                    self.timestamp,
                    self.use_case,
                    self.app_pkg,
                    self.app_version,
                    self.device_model,
                    self.duration,
                    self.energy_consumption,
                ])
            return True

    @classmethod
    def clear_database(cls):
        """ Clear database. Deletes CSV data file.
        """
        try:
            os.remove(cls.csv_storage)
        except OSError:
            pass
