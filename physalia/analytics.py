"""Provides functions for data analysis of Measurements."""

from statsmodels.graphics.boxplots import violinplot as stats_violinplot
# from physalia.models import Measurement

def violinplot(*samples):
    """Create violin plot for a set of measurement samples."""
    consumptions = [
        [measurement.energy_consumption for measurement in sample]
        for sample in samples
    ]
    labels = [
        len(sample) > 0 and sample[0].use_case.title().replace('_', ' ')
        for sample in samples
    ]
    stats_violinplot(consumptions, labels=labels)
