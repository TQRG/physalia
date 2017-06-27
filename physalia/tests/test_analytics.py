"""Test analytics module."""

import unittest

import matplotlib.pyplot as plt
from physalia.analytics import violinplot
from physalia.fixtures.models import create_random_sample

# pylint: disable=missing-docstring

class TestAnalytics(unittest.TestCase):

    def test_violinplot(self):
        # pylint: disable=no-self-use
        sample_a = create_random_sample(10, 1, use_case='login_fb')
        sample_b = create_random_sample(20, 0.5, use_case='login_twitter')
        # sample_c = create_random_sample(15, 3, use_case='login_google+')
        violinplot(sample_a, sample_b)
        plt.savefig("./physalia/tests/tmp/violinplot.png")
