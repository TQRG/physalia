"""Test analytics module."""

import unittest
from tempfile import NamedTemporaryFile

from mock import patch, MagicMock

from physalia.analytics import violinplot
from physalia.fixtures.models import create_random_sample, create_random_samples
from physalia.analytics import hypothesis_test, fancy_hypothesis_test, smart_hypothesis_testing
from physalia.utils.symbols import GREEK_ALPHABET


# pylint: disable=missing-docstring

class TestAnalytics(unittest.TestCase):

    def test_violinplot(self):
        # pylint: disable=no-self-use
        sample_a = create_random_sample(10, 1, use_case='login_fb')
        sample_b = create_random_sample(20, 0.5, use_case='login_twitter')
        sample_c = create_random_sample(15, 3, use_case='login_google+')
        with NamedTemporaryFile(prefix="violinplot",
                                suffix='.png', delete=False) as tmp_file:
            violinplot(sample_a, sample_b, sample_c,
                       save_fig=tmp_file)

    def test_hypothesis_test(self):
        sample_a, sample_b = create_random_samples()
        _, pvalue = hypothesis_test(sample_a, sample_b)
        self.assertLess(pvalue, 0.05)

    def test_fancy_hypothesis_test(self):
        try:
            from StringIO import StringIO
        except ImportError:
            from io import StringIO
        from string import Template

        # sample_a, sample_b = create_random_samples()
        with patch('physalia.analytics.hypothesis_test',
                   MagicMock(return_value=(0, 0.0001))):
            out = StringIO()
            fancy_hypothesis_test(
                None, None,
                "login with email",
                "login with facebook",
                out=out
            )
            output = out.getvalue()

            self.assertEqual(
                output,
                Template(
                    "Hypothesis testing:\n"
                    "\t$H0: $mu login with email = $mu login with facebook.\n"
                    "\t$H1: $mu login with email $neq $mu login with facebook.\n"
                    "\n"
                    "Applying Welch's t-test with $alpha=0.05, the null"
                    " hypothesis is rejected (p-value=<0.001).\n"
                    "Thus, one can say that the means of populations"
                    " \"login with email\" and \"login with facebook\" are"
                    " different.\n"
                ).substitute(GREEK_ALPHABET)
            )
        with patch('physalia.analytics.hypothesis_test',
                   MagicMock(return_value=(0, 0.061231))):
            out = StringIO()
            fancy_hypothesis_test(
                None, None,
                "login with email",
                "login with facebook",
                out=out
            )
            output = out.getvalue()
            self.assertEqual(
                output,
                Template(
                    "Hypothesis testing:\n"
                    "\t$H0: $mu login with email = $mu login with facebook.\n"
                    "\t$H1: $mu login with email $neq $mu login with facebook.\n"
                    "\n"
                    "Applying Welch's t-test with $alpha=0.05, the null"
                    " hypothesis is not rejected (p-value=0.061).\n"
                    "Thus, it was not possible to find evidence that"
                    " the means of populations login with email and "
                    "login with facebook are different.\n"
                ).substitute(GREEK_ALPHABET)
            )

    def test_smart_hypothesis_testing(self):
        # pylint: disable=no-self-use
        sample_a = create_random_sample(10, 1, use_case='login_fb')
        sample_b = create_random_sample(20, 0.5, use_case='login_twitter')
        sample_c = create_random_sample(15, 3, use_case='login_google+')
        with NamedTemporaryFile(
            prefix="violinplot",
            suffix='.tex', delete=False
        ) as tmp_file, open(tmp_file.name, "w") as out:
            smart_hypothesis_testing(
                sample_a, sample_b, sample_c,
                fancy="True", alpha=0.05, equal_var=True,
                out=out
            )
