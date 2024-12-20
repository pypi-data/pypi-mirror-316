"""
This module provides statistical analysis tools.
"""

import numpy as np
from scipy import stats

class StatisticalAnalysis:
    """
    A class for performing statistical analyses.
    """

    @staticmethod
    def calculate_mean(data):
        """
        Calculate the mean of the given data.

        Args:
            data (array-like): Input data.

        Returns:
            float: Mean of the data.
        """
        return np.mean(data)

    @staticmethod
    def calculate_median(data):
        """
        Calculate the median of the given data.

        Args:
            data (array-like): Input data.

        Returns:
            float: Median of the data.
        """
        return np.median(data)

    @staticmethod
    def calculate_mode(data):
        """
        Calculate the mode of the given data.

        Args:
            data (array-like): Input data.

        Returns:
            array: Mode(s) of the data.
        """
        return stats.mode(data).mode

    @staticmethod
    def calculate_std(data):
        """
        Calculate the standard deviation of the given data.

        Args:
            data (array-like): Input data.

        Returns:
            float: Standard deviation of the data.
        """
        return np.std(data)

    @staticmethod
    def calculate_correlation(x, y):
        """
        Calculate the Pearson correlation coefficient between two variables.

        Args:
            x (array-like): First variable.
            y (array-like): Second variable.

        Returns:
            float: Pearson correlation coefficient.
        """
        return np.corrcoef(x, y)[0, 1]

    @staticmethod
    def perform_ttest(group1, group2):
        """
        Perform an independent t-test between two groups.

        Args:
            group1 (array-like): First group of data.
            group2 (array-like): Second group of data.

        Returns:
            tuple: T-statistic and p-value.
        """
        return stats.ttest_ind(group1, group2)

    @staticmethod
    def perform_chi_square(observed, expected):
        """
        Perform a chi-square test.

        Args:
            observed (array-like): Observed frequencies.
            expected (array-like): Expected frequencies.

        Returns:
            tuple: Chi-square statistic and p-value.
        """
        return stats.chisquare(observed, expected)

