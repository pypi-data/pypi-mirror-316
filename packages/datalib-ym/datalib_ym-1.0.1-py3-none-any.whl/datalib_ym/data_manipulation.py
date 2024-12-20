"""
This module provides classes for data loading and transformation.
"""

import pandas as pd
import numpy as np

class DataLoader:
    """
    A class for loading and basic processing of CSV files.
    """

    def __init__(self):
        self.data = None

    def load_csv(self, file_path):
        """
        Load a CSV file into a pandas DataFrame.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            pandas.DataFrame: Loaded data.
        """
        self.data = pd.read_csv(file_path)
        return self.data

    def save_csv(self, file_path):
        """
        Save the current data to a CSV file.

        Args:
            file_path (str): Path to save the CSV file.
        """
        if self.data is not None:
            self.data.to_csv(file_path, index=False)
        else:
            raise ValueError("No data to save. Load data first.")

    def filter_data(self, condition):
        """
        Filter the data based on a given condition.

        Args:
            condition (str): A string representing a boolean condition.

        Returns:
            pandas.DataFrame: Filtered data.
        """
        if self.data is not None:
            return self.data.query(condition)
        else:
            raise ValueError("No data to filter. Load data first.")

class DataTransformer:
    """
    A class for transforming and preprocessing data.
    """

    @staticmethod
    def normalize(data, method='zscore'):
        """
        Normalize the given data.

        Args:
            data (pandas.DataFrame): Data to normalize.
            method (str): Normalization method ('zscore' or 'minmax').

        Returns:
            pandas.DataFrame: Normalized data.
        """
        if method == 'zscore':
            return (data - data.mean()) / data.std()
        elif method == 'minmax':
            return (data - data.min()) / (data.max() - data.min())
        else:
            raise ValueError("Invalid normalization method. Use 'zscore' or 'minmax'.")

    @staticmethod
    def handle_missing_values(data, strategy='mean'):
        """
        Handle missing values in the data.

        Args:
            data (pandas.DataFrame): Data with missing values.
            strategy (str): Strategy to handle missing values ('mean', 'median', or 'mode').

        Returns:
            pandas.DataFrame: Data with handled missing values.
        """
        if strategy == 'mean':
            return data.fillna(data.mean())
        elif strategy == 'median':
            return data.fillna(data.median())
        elif strategy == 'mode':
            return data.fillna(data.mode().iloc[0])
        else:
            raise ValueError("Invalid strategy. Use 'mean', 'median', or 'mode'.")

