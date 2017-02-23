"""Asserts to use in energy tests."""

import numpy
from physalia.models import Measurement

def consumption_below(sample, energy_consumption_baseline):
    """Test for energy consumption lower than a given value in Joules (avg).

    Args:
        sample (list of Measurement): sample of measurements
        energy_consumption (number): baseline energy consumption in Joules.
    """
    energy_consumption_mean = Measurement.mean_energy_consumption(sample)
    assert energy_consumption_mean < energy_consumption_baseline


def consumption_lower_than_app(sample, app, use_case=None):
    """Test that a given sample spends less energy than a known app.

    Args:
        sample (list of Measurement): sample of measurements
        app (string): identifier/package of the app to be compared
        use_case (string): select only data from a given use case
    """
    pass

def top_percentile(sample, nth, app=None, use_case=None):
    """Test that a given sample is in the top nth percentile.
    
    Args:
        sample (list of Measurement): sample of measurements
        nth (number): percentage of the position in which the sample should fit
        app (string): identifier of the application within the sample should be compared
        use_case (string: identifier of the use case used to create the ranking
    """
    pass
