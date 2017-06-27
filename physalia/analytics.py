"""Provides functions for data analysis of Measurements."""

import sys
from string import Template
from statsmodels.graphics.boxplots import violinplot as stats_violinplot
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

from physalia.utils.symbols import GREEK_ALPHABET



def violinplot(*samples, **options):
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
    if options.get('save_fig'):
        plt.savefig(options.get('save_fig'))
    if options.get('show_fig'):
        plt.show()

def hypothesis_test(sample_a, sample_b):
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

def fancy_hypothesis_test(sample_a, sample_b,
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
    test, pvalue = hypothesis_test(sample_a, sample_b)
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
              u" hypothesis is{negate} rejected (p-value={pvalue}).\n".format(
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
    return (test, pvalue)
