"""
DataLib: A comprehensive library for data manipulation, analysis, and visualization.

This library provides tools for:
- Data manipulation
- Statistical analysis
- Data visualization
- Advanced analysis techniques
"""

from .data_manipulation import DataLoader, DataTransformer
from .statistics import StatisticalAnalysis
from .visualization import DataVisualizer
from .advanced_analysis import Regression, Classification, Clustering

__version__ = "0.1.0"
__all__ = ['DataLoader', 'DataTransformer', 'StatisticalAnalysis', 'DataVisualizer', 'Regression', 'Classification', 'Clustering']

