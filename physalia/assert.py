"""Asserts to use in energy tests."""

def consumption_lower_than(sample, energy_consumption):
    """Test for energy consumption lower than a given value in Joules (avg).

    Args:
        sample (list of Measurement): sample of measurements
        energy_consumption (number): baseline energy consumption in Joules.
    """
    pass

def top_percentile(sample, nth, app, use_case=None):
    """Test that a given sample is in the top nth percentile."""
    pass

def better_than(sample, app, use_case=None):
    """Test that a given sample spends less energy than a known app."""
    pass
