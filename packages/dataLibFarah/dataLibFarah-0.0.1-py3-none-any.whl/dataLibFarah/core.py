import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.stats import ttest_ind, chi2_contingency

class DataLib:
    """
    A library for data manipulation, analysis, and visualization.
    """

    @staticmethod
    def load_csv(file_path):
        """Load a CSV file into a DataFrame."""
        return pd.read_csv(file_path)

    @staticmethod
    def save_csv(dataframe, file_path):
        """Save a DataFrame to a CSV file."""
        dataframe.to_csv(file_path, index=False)

    @staticmethod
    def normalize_data(dataframe):
        """Normalize numerical columns in a DataFrame."""
        return (dataframe - dataframe.min()) / (dataframe.max() - dataframe.min())

    @staticmethod
    def handle_missing_values(dataframe, method="mean"):
        """Handle missing values in a DataFrame by a specified method."""
        if method == "mean":
            return dataframe.fillna(dataframe.mean())
        elif method == "median":
            return dataframe.fillna(dataframe.median())
        elif method == "mode":
            return dataframe.fillna(dataframe.mode().iloc[0])
        else:
            raise ValueError("Unsupported method for handling missing values.")

    @staticmethod
    def calculate_statistics(dataframe):
        """Calculate basic statistics for numerical columns."""
        return dataframe.describe()

    @staticmethod
    def mean(data):
        """Calculate the mean of a numerical dataset."""
        return np.mean(data)

    @staticmethod
    def median(data):
        """Calculate the median of a numerical dataset."""
        return np.median(data)

    @staticmethod
    def mode(data):
        """Calculate the mode of a numerical dataset."""
        return data.mode().iloc[0]

    @staticmethod
    def standard_deviation(data):
        """Calculate the standard deviation of a numerical dataset."""
        return np.std(data)

    @staticmethod
    def t_test(sample1, sample2):
        """Perform an independent T-test between two samples."""
        stat, p_value = ttest_ind(sample1, sample2)
        return stat, p_value

    @staticmethod
    def chi_squared_test(observed, expected):
        """Perform a chi-squared test."""
        chi2, p_value, dof, _ = chi2_contingency([observed, expected])
        return chi2, p_value, dof

    @staticmethod
    def correlation_matrix(dataframe):
        """Generate and plot a correlation matrix."""
        correlation = dataframe.corr()
        plt.figure(figsize=(10, 8))
        plt.matshow(correlation, cmap="coolwarm", fignum=1)
        plt.colorbar()
        plt.xticks(range(len(correlation.columns)), correlation.columns, rotation=90)
        plt.yticks(range(len(correlation.columns)), correlation.columns)
        plt.show()
        return correlation

    @staticmethod
    def plot_data(dataframe, x_column, y_column, kind="scatter"):
        """Generate a plot of data from two columns."""
        if kind == "scatter":
            dataframe.plot.scatter(x=x_column, y=y_column)
        elif kind == "bar":
            dataframe.plot.bar(x=x_column, y=y_column)
        elif kind == "hist":
            dataframe[y_column].plot.hist()
        else:
            raise ValueError("Unsupported plot kind.")
        plt.show()

    @staticmethod
    def linear_regression(x, y):
        """Perform linear regression and return the model and coefficients."""
        model = LinearRegression()
        model.fit(x, y)
        return model, model.coef_, model.intercept_

    @staticmethod
    def polynomial_regression(x, y, degree):
        """Perform polynomial regression and return the model and coefficients."""
        from numpy.polynomial.polynomial import Polynomial
        poly_model = Polynomial.fit(x.flatten(), y.flatten(), degree)
        return poly_model, poly_model.convert().coef

    @staticmethod
    def apply_pca(data, n_components=2):
        """Perform Principal Component Analysis (PCA) on the data."""
        pca = PCA(n_components=n_components)
        transformed_data = pca.fit_transform(data)
        return transformed_data, pca.explained_variance_ratio_

    @staticmethod
    def kmeans_clustering(data, n_clusters):
        """Apply k-means clustering to the data."""
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        clusters = kmeans.fit_predict(data)
        return clusters, kmeans.cluster_centers_

    @staticmethod
    def knn_classification(train_data, train_labels, test_data, k=3):
        """Perform k-NN classification."""
        from sklearn.neighbors import KNeighborsClassifier
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(train_data, train_labels)
        return knn.predict(test_data)

    @staticmethod
    def decision_tree_classification(train_data, train_labels, test_data):
        """Perform Decision Tree classification."""
        from sklearn.tree import DecisionTreeClassifier
        dt = DecisionTreeClassifier()
        dt.fit(train_data, train_labels)
        return dt.predict(test_data)

