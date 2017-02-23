"""Fixtures for models module."""

from physalia.models import Measurement
import numpy


def create_measurement(use_case='login',
                       app_pkg='com.package',
                       duration=2,
                       energy_consumption=30):
    """Fake data for measurement."""
    return Measurement(
        1485634263.096069,  # timestamp
        use_case,           # use_case
        app_pkg,            # application package
        '1.0.0',            # version
        'Nexus 5X',         # device model
        duration,           # duration
        energy_consumption  # energy consumption
    )

def create_random_sample(mean, std,
                         app_pkg='com.package',
                         use_case='login',
                         count=30, seed=1):
    """Create a sample of measurements."""
    # pylint: disable=too-many-arguments
    if seed is not None:
        numpy.random.seed(seed)
    energy_consumptions = numpy.random.normal(loc=mean,
                                              scale=std,
                                              size=count)
    return [
        create_measurement(
            energy_consumption=energy_consumptions[i],
            app_pkg=app_pkg,
            use_case=use_case
        )
        for i in range(count)
    ]

def create_random_samples(count=30, seed=1):
    """Create a sample of measurements."""
    if seed is not None:
        numpy.random.seed(seed)
    sample_a = create_random_sample(10.0, 1.0, count=count, seed=None)
    sample_b = create_random_sample(12.0, 1.0, count=count, seed=None)
    return sample_a, sample_b
