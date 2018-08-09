"""Models that require persistence."""

import csv
import os
from pathlib import Path

from itertools import groupby
from collections import OrderedDict
from operator import itemgetter
import bisect
import numpy

class Measurement(object):
    """Energy measurement information.

    Attributes:
        timestamp               When the execution started.
        use_case                Key identifier of the use case.
        app_pkg                 Package of the app.
        app_version             Version of the app.
        device_model            Device where the measurements were performed.
        duration                Time it takes to execute the use case.
        energy_consumption      Mean of the measurements.
        power_meter             Name of the power meter used.

    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    csv_storage = "./db.csv"
    COLUMN_APP_PKG = 2
    COLUMN_USE_CASE = 1
    COLUMN_NAME = COLUMN_USE_CASE

    def __init__(
            self,
            timestamp,
            use_case,
            app_pkg,
            app_version,
            device_model,
            duration,
            energy_consumption,
            power_meter="NA",
            success=True,
            notes=None,
    ):  # noqa: D102,D107
        self.persisted = False
        self.timestamp = float(timestamp)
        self.use_case = use_case
        self.app_pkg = app_pkg
        self.app_version = app_version
        self.device_model = device_model
        self.duration = float(duration)
        self.energy_consumption = float(energy_consumption)
        self.power_meter = power_meter
        self.success = success
        self.notes = notes

    def persist(self):
        """Store measurement in the database."""
        if self.persisted:
            return False
        self.save_to_csv(self.csv_storage)
        self.persisted = True
        return True

    def save_to_csv(self, filename):
        """Store measurements in a CSV file."""
        if not Path(filename).is_file():
            with open(filename, 'wt') as csvfile:
                csv_writer = csv.writer(csvfile)
                writer.writeheader()
                csv_writer.writerow([
                    "timestamp",
                    "use_case",
                    "app_pkg",
                    "app_version",
                    "device_model",
                    "duration",
                    "energy_consumption",
                    "power_meter",
                    "success",
                    "notes",
                ])
        with open(filename, 'at') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([
                self.timestamp,
                self.use_case,
                self.app_pkg,
                self.app_version,
                self.device_model,
                self.duration,
                self.energy_consumption,
                self.power_meter,
                self.success,
                self.notes,
            ])

    def __str__(self):
        """Get description of the measurement."""
        return (
            "Measurement for {}:\n"
            "  {: <20}{:.4f}J\n"
            "  {: <20}{}s\n"
            "  {: <20}{}\n"
            "  {: <20}{}"
        ).format(self.use_case,
                 "Energy consumption:", self.energy_consumption,
                 "Duration:", self.duration,
                 "Power meter:", self.power_meter,
                 "Phone:", self.device_model)

    def __repr__(self):
        """Get representation of the measurement."""
        return (
            "Measurement("
            "use_case={use_case!r}, "
            "energy_consumption={energy_consumption!r}, "
            "duration={duration!r}, "
            "power_meter={power_meter!r}, "
            "device_model={device_model!r},"
            "success={success!r}"
            ")".format(**self.__dict__)
        )

    def __float__(self):
        """Convert measurement to float using energy consumption."""
        return self.energy_consumption

    @classmethod
    def clear_database(cls):
        """Clear database. Deletes CSV data file."""
        try:
            os.remove(cls.csv_storage)
        except OSError:
            pass

    @classmethod
    def _get_unique_from_column(cls, column_index):
        """Get unique values of the given column."""
        with open(cls.csv_storage, 'rt') as csvfile:
            csv_reader = csv.reader(csvfile)
            return {row[column_index] for row in csv_reader}

    @classmethod
    def get_unique_apps(cls):
        """Get all unique apps existing in the database.

        Returns:
            List of unique apps.

        """
        return cls._get_unique_from_column(cls.COLUMN_APP_PKG)

    @classmethod
    def get_unique_use_cases(cls, measurements):
        """Get all unique use cases.

        Returns:
            List of unique use cases.

        """
        return {
            measurement.use_case
            for measurement in measurements
        }

    @classmethod
    def get_all_entries_of_app(cls, app, use_case):
        """Get all entries that have a specific app and use case.

        If the use_case is None, all use_cases are retrieved.
        """
        with open(cls.csv_storage, 'rt') as csvfile:
            csv_reader = csv.reader(csvfile)
            return [
                Measurement(*row) for row in csv_reader
                if row[cls.COLUMN_USE_CASE] == use_case or use_case is None and
                row[cls.COLUMN_APP_PKG] == app
            ]

    @classmethod
    def get_entries_with_name_like(cls, name, measurements):
        """Get all measurements with a similar name to `name`."""
        return (
            measurement for measurement in measurements
            if name in measurement.use_case
        )

    @classmethod
    def get_entries_with_name(cls, name, measurements):
        """Get all measurements with a given name."""
        return (
            measurement for measurement in measurements
            if name == measurement.use_case
        )

    @classmethod # deleteme
    def mean_energy_consumption(cls, measurements):
        """Get mean energy consumption from a set of measurements."""
        len_measurements = len(measurements)
        if len_measurements == 0:
            raise Exception("Empty sample.")

        energy_consumptions = [
            float(measurement.energy_consumption)
            for measurement in measurements
        ]
        return sum(energy_consumptions) / len_measurements

    @classmethod
    def describe(cls, measurements):
        """Descriptive statistics for a set of measurements.

        Get descriptive statistics for time and energy
        consumption for a set of measurements.

        Returns:
            Tuple of Energy consumption mean, std, Duration mean, std.

        """
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

    @classmethod
    def describe_app_use_case(cls, app, use_case):
        """Descriptive statistics for a stored App use case.

        Get descriptive statistics for time and energy
        consumption of an application use case.

        Args:
            app (string): Application package.
            use_case (string): Name of the use case

        Returns:
            Tuple of Energy consumption mean, std, Duration mean, std.

        """
        measurements = cls.get_all_entries_of_app(app, use_case)
        return cls.describe(measurements)


    @classmethod
    def get_energy_ranking(cls):
        """Ranking of the energy consumption of all apps.

        Get apps aggregated and sorted by mean energy consumption.

        Returns:
            OrderedDict with key=app_pkg and value=energy_consumption

        """
        with open(cls.csv_storage, 'rt') as csvfile:
            csv_reader = csv.reader(csvfile)

            data = [Measurement(*row) for row in csv_reader]
            data = sorted(data, key=lambda msrmnt: msrmnt.app_pkg)
            grouped_data = {
                k: Measurement.mean_energy_consumption(list(group))
                for (k, group) in groupby(
                    data,
                    key=lambda msrmnt: msrmnt.app_pkg
                )
            }
            sorted_data = OrderedDict(sorted(
                list(grouped_data.items()),
                key=itemgetter(1)
            ))
            return sorted_data

    @classmethod
    def get_position_in_ranking(cls, measurements):
        """Get the position in ranking of a given sample of measurements."""
        energy_ranking = cls.get_energy_ranking()
        consumptions = list(energy_ranking.values())
        energy_consumption = cls.mean_energy_consumption(measurements)
        return (
            bisect.bisect_left(consumptions, energy_consumption)+1,
            len(consumptions)
        )
