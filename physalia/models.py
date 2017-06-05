"""Models that require persistence."""

import csv
import os
import sys
from string import Template
from itertools import groupby
from collections import OrderedDict
import bisect
from scipy.stats import ttest_ind
import numpy
from physalia.utils.symbols import GREEK_ALPHABET

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

    def __init__(
            self,
            timestamp,
            use_case,
            app_pkg,
            app_version,
            device_model,
            duration,
            energy_consumption,
            power_meter="NA"
    ):  # noqa: D102
        self.persisted = False
        self.timestamp = timestamp
        self.use_case = use_case
        self.app_pkg = app_pkg
        self.app_version = app_version
        self.device_model = device_model
        self.duration = duration
        self.energy_consumption = energy_consumption
        self.power_meter = power_meter

    def persist(self):
        """Store measurement in the database."""
        if self.persisted:
            return False
        self.save_to_csv(self.csv_storage)
        self.persisted = True
        return True

    def save_to_csv(self, filename):
        """Store measurements in a CSV file."""
        with open(filename, 'a') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([
                self.timestamp,
                self.use_case,
                self.app_pkg,
                self.app_version,
                self.device_model,
                self.duration,
                self.energy_consumption,
                self.power_meter
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
        with open(cls.csv_storage, 'rb') as csvfile:
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
    def get_unique_use_cases(cls):
        """Get all unique use cases.

        Returns:
            List of unique use cases.

        """
        return cls._get_unique_from_column(cls.COLUMN_USE_CASE)

    @classmethod
    def get_all_entries_of_app(cls, app, use_case):
        """Get all entries that have a specific app and use case.

        If the use_case is None, all use_cases are retrieved.
        """
        with open(cls.csv_storage, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile)
            return [
                Measurement(*row) for row in csv_reader
                if row[cls.COLUMN_USE_CASE] == use_case or use_case is None and
                row[cls.COLUMN_APP_PKG] == app
            ]

    @classmethod
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
    def hypothesis_test(cls, sample_a, sample_b):
        """Perform hypothesis test over two samples of measurements.

        Uses Welch's t-test to check whether energy consumption
        is different in the populations of samples a and b.

        Args:
            sample_a (list of Measurement): measurements of sample a
            sample_b (list of Measurement): measurements of sample b

        Returns:
            t (float): The calculated t-statistic
            prob (float): The two-tailed p-value

        """
        return ttest_ind(
            [measurement.energy_consumption for measurement in sample_a],
            [measurement.energy_consumption for measurement in sample_b],
            equal_var=False
        )

    @classmethod
    def fancy_hypothesis_test(cls, sample_a, sample_b,
                              name_a, name_b, out=sys.stdout):
        """Perform and describe hypothesis testing of 2 samples.

        Args:
            sample_a (list of Measurement): measurements of sample a
            sample_b (list of Measurement): measurements of sample b
            sample_a (String): population name of sample a
            sample_b (String): population name of sample b
            out (file): data stream for output

        """
        alpha = 0.05
        _, pvalue = cls.hypothesis_test(sample_a, sample_b)
        rejected_null_h = alpha <= pvalue
        out.write(
            Template(
                "Hypothesis testing:\n"
                "\t$H0: $mu {name_a} = $mu {name_b}.\n"
                "\t$H1: $mu {name_a} $neq $mu {name_b}.\n"
                "\n"
            ).substitute(GREEK_ALPHABET).format(name_a=name_a,
                                                name_b=name_b)
        )
        out.write(u"Applying Welch's t-test with {alpha_letter}=0.05, the null"
                  " hypothesis is{negate} rejected (p-value={pvalue}).\n".format(
                      negate=" not" if rejected_null_h else "",
                      pvalue="<0.001" if pvalue < 0.001 else "{:.3f}".format(pvalue),
                      alpha_letter=GREEK_ALPHABET['alpha']
                  ))

        if rejected_null_h:
            out.write("Thus, it was not possible to find evidence that"
                      " the means of populations {name_a} and {name_b}"
                      " are different.\n".format(name_a=name_a,
                                                 name_b=name_b))
        else:
            out.write("Thus, one can say that the means of populations"
                      " \"{name_a}\" and \"{name_b}\" are different.\n"
                      "".format(name_a=name_a, name_b=name_b))
        return cls.hypothesis_test(sample_a, sample_b)

    @classmethod
    def get_energy_ranking(cls):
        """Ranking of the energy consumption of all apps.

        Get apps aggregated and sorted by mean energy consumption.

        Returns:
            OrderedDict with key=app_pkg and value=energy_consumption

        """
        with open(cls.csv_storage, 'rb') as csvfile:
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
                grouped_data.items(),
                key=lambda (key, energy_consumption): energy_consumption
            ))
            return sorted_data

    @classmethod
    def get_position_in_ranking(cls, measurements):
        """Get the position in ranking of a given sample of measurements."""
        energy_ranking = cls.get_energy_ranking()
        consumptions = energy_ranking.values()
        energy_consumption = cls.mean_energy_consumption(measurements)
        return (
            bisect.bisect_left(consumptions, energy_consumption)+1,
            len(consumptions)
        )
