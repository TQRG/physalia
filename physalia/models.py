"""Models that require persistence
"""

import csv
import os
import numpy


class Measurement(object):
    """Class for with energy measurement information

    Attributes:
        timestamp               When the execution started.
        use_case                Key identifier of the use case.
        app_pkg                 Package of the app.
        app_version             Version of the app.
        device_model            Device where the measurements were performed.
        duration                Time it takes to execute the use case.
        energy_consumption      Mean of the measurements.
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    csv_storage = "./db.csv"
    COLUMN_APP_PKG = 2
    COLUMN_USE_CASE = 1

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
            self.persisted = True
            return True

    @classmethod
    def clear_database(cls):
        """ Clear database. Deletes CSV data file.
        """
        try:
            os.remove(cls.csv_storage)
        except OSError:
            pass

    @classmethod
    def _get_unique_from_column(cls, column_index):
        """ Get unique values of the given column
        """
        with open(cls.csv_storage, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile)
            return {row[column_index] for row in csv_reader}

    @classmethod
    def get_unique_apps(cls):
        """ Get all unique apps existing in the database
        """
        return cls._get_unique_from_column(cls.COLUMN_APP_PKG)

    @classmethod
    def get_unique_use_cases(cls):
        """ Get all unique use cases
        """
        return cls._get_unique_from_column(cls.COLUMN_USE_CASE)

    @classmethod
    def get_all_entries_of_app_use_case(cls, app, use_case):
        """ Get all entries that have a specific app and use case
        """
        with open(cls.csv_storage, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile)
            return [
                Measurement(*row) for row in csv_reader
                if row[cls.COLUMN_USE_CASE] == use_case and
                row[cls.COLUMN_APP_PKG] == app
            ]

    @classmethod
    def describe_app_use_case(cls, app, use_case):
        """ Get descriptive statistics for time and energy
        consumption of an application use case

        Args:
            app (string): Application package.
            use_case (string): Name of the use case

        Returns:
            Tuple of Energy consumption mean, std, Duration mean, std.
        """
        measurements = cls.get_all_entries_of_app_use_case(app, use_case)
        len_measurements = len(measurements)
        if len_measurements == 0:
            return

        energy_consumptions = [
            float(measurement.energy_consumption)
            for measurement in measurements
        ]
        energy_consumption_mean = sum(energy_consumptions) / len_measurements
        energy_consumption_std = numpy.std(energy_consumptions)

        durations = [
            float(measurement.duration)
            for measurement in measurements
        ]
        duration_mean = sum(durations) / len_measurements
        duration_std = numpy.std(durations)
        return (
            energy_consumption_mean,
            energy_consumption_std,
            duration_mean,
            duration_std,
        )
