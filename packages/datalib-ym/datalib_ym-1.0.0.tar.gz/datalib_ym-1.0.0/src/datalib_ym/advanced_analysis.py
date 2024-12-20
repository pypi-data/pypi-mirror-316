"""
This module provides advanced data analysis tools.
"""

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score

class Regression:
    """
    A class for performing regression analysis.
    """

    @staticmethod
    def linear_regression(X, y):
        """
        Perform linear regression.

        Args:
            X (array-like): Features.
            y (array-like): Target variable.

        Returns:
            tuple: Fitted model and mean squared error.
        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        return model, mse

    @staticmethod
    def polynomial_regression(X, y, degree=2):
        """
        Perform polynomial regression.

        Args:
            X (array-like): Features.
            y (array-like): Target variable.
            degree (int): Degree of the polynomial.

        Returns:
            tuple: Fitted model and mean squared error.
        """
        X_poly = PolynomialFeatures(degree=degree).fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        return model, mse

class Classification:
    """
    A class for performing classification analysis.
    """

    @staticmethod
    def logistic_regression(X, y):
        """
        Perform logistic regression.

        Args:
            X (array-like): Features.
            y (array-like): Target variable.

        Returns:
            tuple: Fitted model and accuracy score.
        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LogisticRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return model, accuracy

    @staticmethod
    def decision_tree(X, y):
        """
        Perform decision tree classification.

        Args:
            X (array-like): Features.
            y (array-like): Target variable.

        Returns:
            tuple: Fitted model and accuracy score.
        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = DecisionTreeClassifier()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return model, accuracy

    @staticmethod
    def knn(X, y, n_neighbors=5):
        """
        Perform k-Nearest Neighbors classification.

        Args:
            X (array-like): Features.
            y (array-like): Target variable.
            n_neighbors (int): Number of neighbors.

        Returns:
            tuple: Fitted model and accuracy score.
        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = KNeighborsClassifier(n_neighbors=n_neighbors)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return model, accuracy

class Clustering:
    """
    A class for performing clustering analysis.
    """

    @staticmethod
    def kmeans(X, n_clusters=3):
        """
        Perform k-means clustering.

        Args:
            X (array-like): Features.
            n_clusters (int): Number of clusters.

        Returns:
            KMeans: Fitted k-means model.
        """
        model = KMeans(n_clusters=n_clusters, random_state=42)
        model.fit(X)
        return model

    @staticmethod
    def pca(X, n_components=2):
        """
        Perform Principal Component Analysis (PCA).

        Args:
            X (array-like): Features.
            n_components (int): Number of components to keep.

        Returns:
            tuple: Fitted PCA model and transformed data.
        """
        model = PCA(n_components=n_components)
        transformed_data = model.fit_transform(X)
        return model, transformed_data

