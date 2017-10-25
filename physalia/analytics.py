"""Provides functions for data analysis of Measurements."""

import sys
from string import Template
from operator import itemgetter
from collections import OrderedDict
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


from tabulate import tabulate
import tabulate as T
from scipy.stats import ttest_ind
from scipy.stats import f_oneway
# normality tests
from scipy.stats import normaltest, shapiro
import numpy as np

from physalia.utils.symbols import GREEK_ALPHABET

# pylint: disable=wrong-import-position
# Matplotlib is a special case
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from statsmodels.graphics.boxplots import violinplot as stats_violinplot


def violinplot(*samples, **options):
    """Create violin plot for a set of measurement samples."""
    names_dict = options.get("names_dict")
    title = options.get("title")
    sort = options.get("sort")
    millijoules = options.get("millijoules")

    consumptions = [np.array(sample, dtype='float') for sample in samples]
    if millijoules:
        for sample in consumptions:
            sample *= 1000
        unit = 'mJ'
    else:
        unit = 'J'

    if names_dict:
        labels = [
            sample and names_dict[sample[0].use_case]
            for sample in samples
        ]
    else:
        labels = [
            sample and sample[0].use_case.title().replace('_', ' ')
            for sample in samples
        ]

    if sort:
        labels, samples = zip(*sorted(zip(labels, samples)))

    stats_violinplot(consumptions, labels=labels, plot_opts={'label_rotation': 90})
    plt.gcf().subplots_adjust(bottom=0.3, left=0.1, right=0.999, top=0.99)
    axes = plt.gca()
    axes.set_ylim(bottom=0.0)
    axes.set_ylabel("Energy ({})".format(unit))
    axes.spines['right'].set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.yaxis.grid(linestyle='dashed')
    axes.yaxis.set_ticks_position('none')

    if title:
        plt.title(title)
    if options.get('save_fig'):
        plt.savefig(options.get('save_fig'))
    if options.get('show_fig'):
        plt.show()


def samples_are_normal(*samples, **options):
    """Test whether each sample differs from a normal distribution.

    Use both Shapiro-Wilk test and D'Agostino and Pearson's test
    to test the null hypothesis that the sample is drawn from a
    normal distribution.

    Returns:
        List of tuples (is_normal(bool),(statistic(float),pvalue(float)).

    """
    alpha = options.get('alpha', 0.05)
    results = []
    for sample in samples:
        (_, shapiro_pvalue) = shapiro_result = shapiro(sample)
        (_, normaltest_pvalue) = normaltest_result = normaltest(sample)
        results.append((
            not (normaltest_pvalue < alpha and shapiro_pvalue < alpha),
            shapiro_result,
            normaltest_result
        ))
    return results


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

def _format_test_result(result):
    statistic, pvalue = result
    return u"(test={:.2f}, {})".format(statistic, _pvalue_to_str(pvalue))

def pairwise_welchs_ttest(*samples, **options):
    """Perform pairwise Welch's t-test."""
    names = options.get("names")
    sort = options.get("sort")
    table_fmt = options.get("table_fmt", "grid")
    out = options.get("out", sys.stdout)

    if not names:
        names = [
            sample and sample[0].use_case.title().replace('_', ' ')
            for sample in samples
        ]

    if sort:
        names, samples = zip(*sorted(zip(names, samples)))

    samples = [np.array(sample, dtype='float') for sample in samples]
    len_samples = len(samples)
    table = list()
    for index, sample_one in enumerate(samples):
        row = list()
        for sample_two in samples[:index]:
            row.append(_format_test_result(ttest_ind(
                sample_one, sample_two,
                equal_var=False
            )))
        row.extend(["--"]*(len_samples-index))
        table.append(row)
    out.write(tabulate(table, headers=names, showindex=names, tablefmt=table_fmt))
    out.write("\n")

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
    out.write(
        u"Applying Welch's t-test with {alpha_letter}=0.05, the null"
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

def smart_hypothesis_testing(*samples, **options):
    """Do a smart hypothesis testing."""
    fancy = options.get('fancy', True)
    out = options.get('out', sys.stdout)
    alpha = options.get('alpha', 0.05)
    equal_var = options.get('equal_var', True)
    latex = options.get('latex', True)

    samples = [np.array(sample, dtype='float') for sample in samples]
    len_samples = len(samples)
    out_buffer = StringIO()

    normality_results = samples_are_normal(*samples)
    if all(map(itemgetter(0), normality_results)):
        # all our samples are normal
        if equal_var:
            if fancy:
                out_buffer.write(Template(
                    u"Hypothesis testing:\n\n"
                    "\t$H0: ${mu}1 = ${mu}2{ellipsis} = $mu{len_samples}. "
                    "The means for all groups are equal.\n"
                    "\t$H1: $exists a,b $elementof Samples: ${mu}a $neq ${mu}b. "
                    "At least two of the means are not equal.\n\n"
                    "The significance test one-way analysis of variance (ANOVA) "
                    "was used with a significance level of $alpha={alpha:.2f}.\n"
                    "This test requires that the following "
                    "assumptions are satisfied:\n\n"
                    "1. Samples are independent.\n"
                    "2. Samples are drawn from a normally distributed population.\n"
                    "3. All populations have equal standard deviation.\n\n"
                    "For the assumption of normal distribution two tests were "
                    "performed ($alpha={alpha}): Shapiro Wilk's test "
                    "and D'Agostino and Pearson's test.\n"
                    "None of these tests reject the null hypothesis with "
                    "significance level of $alpha={alpha}, thus it is assumed that data "
                    "follows a normal distribution.\n\n"
                    "").substitute(GREEK_ALPHABET).format(
                        ellipsis=" = ..." if len_samples > 3 else "",
                        **locals()
                    ))
            statistic, pvalue = f_oneway(*samples)
            if fancy:
                if pvalue < alpha:
                    out_buffer.write(
                        u"One can say that samples come from populations "
                        "with different means, since ANOVA rejects the "
                        "null hypothesis "
                        "(statistic={statistic:.2f}, {pvalue_str}).\n"
                        "".format(pvalue_str=_pvalue_to_str(pvalue), **locals())
                    )
                else:
                    out_buffer.write(
                        u"Thus, it was not possible to find evidence that"
                        " the means of populations are different "
                        "(statistic={statistic:.2f},{rho}={pvalue:.2f}).\n"
                        "".format(**locals())
                    )
            _flush_output(out, out_buffer, latex)
            return statistic, pvalue, f_oneway

def _pvalue_to_str(pvalue):
    pvalue_str = "<0.001" if pvalue < 0.001 else "={:.3f}".format(pvalue)
    return u"{}{}".format('p', pvalue_str)

def _flush_output(out, out_buffer, convert_to_latex):
    output = out_buffer.getvalue()
    out_buffer.close()
    if convert_to_latex:
        from pylatexenc.latexencode import utf8tolatex
        output = (
            "\\documentclass{article}\\begin{document}"
            "\\section{Physalia Hypothesis Test}\n" + utf8tolatex(output)
        ).replace(
            GREEK_ALPHABET["H0"], "$H_0$"
        ).replace(
            GREEK_ALPHABET["H1"], "$H_1$"
        ).replace(
            "<", "\\ensuremath{<}"
        ).replace(
            "\n", "\n\n"
        ).replace(
            "1.", '\\begin{enumerate}\n\\item '
        ).replace(
            "2.", '\\item '
        ).replace(
            "3. All populations have equal standard deviation.",
            '\\item All populations have equal standard deviation.\n\\end{enumerate}'
        ) + "\\end{document}"
    out.write(output)

def describe(*samples, **options):
    """Create table with statistic summary of samples.

    Args:
        loop_count
        names
        out
        table_fmt
        float_fmt
        show_ranking
        mili_joules
    """
    # pylint: disable=too-many-locals

    loop_count = options.get("loop_count")
    names = list(options.get("names"))
    out = options.get('out', sys.stdout)
    table_fmt = options.get("table_fmt", "grid")
    float_fmt = options.get("float_fmt", "")
    show_ranking = options.get("ranking")
    mili_joules = options.get("mili_joules")

    consumption_samples = [np.array(sample, dtype='float') for sample in samples]
    if mili_joules:
        for sample in consumption_samples:
            sample *= 1000
        unit = 'mJ'
    else:
        unit = 'J'
    samples_means = np.array([np.mean(sample) for sample in consumption_samples])
    if show_ranking:
        order = samples_means.argsort()
        ranking = order.argsort()

    table = list()
    for index, sample in enumerate(consumption_samples):
        mean = np.mean(sample)
        row = OrderedDict((
            ("N", len(sample)),
            ("$\\bar{{x}}$ ({})".format(unit), mean),
            ("$s$", np.std(sample)),
        ))
        if loop_count:
            #row["Iter."] = loop_count
            row["Single ({})".format(unit)] = mean/loop_count
        if show_ranking:
            row["Rank"] = int(ranking[index]+1)
            if row["Rank"] == 1 and table_fmt == 'latex':
                names[index] = "\\textbf{"+names[index]+"}"
        table.append(row)
    old_escape_rules = T.LATEX_ESCAPE_RULES
    T.LATEX_ESCAPE_RULES = {}
    out.write(T.tabulate(
        table,
        headers='keys', showindex=names,
        tablefmt=table_fmt, floatfmt=float_fmt
    ))
    T.LATEX_ESCAPE_RULES = old_escape_rules
    out.write("\n")
    return table
