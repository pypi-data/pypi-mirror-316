"""
This module provides data visualization tools.
"""

import matplotlib.pyplot as plt
import seaborn as sns

class DataVisualizer:
    """
    A class for creating various data visualizations.
    """

    @staticmethod
    def plot_bar(data, x, y, title='Bar Plot', xlabel='X', ylabel='Y'):
        """
        Create a bar plot.

        Args:
            data (pandas.DataFrame): Input data.
            x (str): Column name for x-axis.
            y (str): Column name for y-axis.
            title (str): Plot title.
            xlabel (str): X-axis label.
            ylabel (str): Y-axis label.
        """
        plt.figure(figsize=(10, 6))
        sns.barplot(x=x, y=y, data=data)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def plot_histogram(data, column, bins=30, title='Histogram', xlabel='Value', ylabel='Frequency'):
        """
        Create a histogram.

        Args:
            data (pandas.DataFrame): Input data.
            column (str): Column name to plot.
            bins (int): Number of bins.
            title (str): Plot title.
            xlabel (str): X-axis label.
            ylabel (str): Y-axis label.
        """
        plt.figure(figsize=(10, 6))
        sns.histplot(data=data, x=column, bins=bins)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def plot_scatter(data, x, y, title='Scatter Plot', xlabel='X', ylabel='Y'):
        """
        Create a scatter plot.

        Args:
            data (pandas.DataFrame): Input data.
            x (str): Column name for x-axis.
            y (str): Column name for y-axis.
            title (str): Plot title.
            xlabel (str): X-axis label.
            ylabel (str): Y-axis label.
        """
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=x, y=y, data=data)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def plot_correlation_matrix(data, title='Correlation Matrix'):
        """
        Create a correlation matrix heatmap.

        Args:
            data (pandas.DataFrame): Input data.
            title (str): Plot title.
        """
        plt.figure(figsize=(12, 10))
        sns.heatmap(data.corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
        plt.title(title)
        plt.show()

