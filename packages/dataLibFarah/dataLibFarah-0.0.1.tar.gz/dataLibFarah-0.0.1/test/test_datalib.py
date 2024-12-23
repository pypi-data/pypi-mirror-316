import pytest
import pandas as pd
import numpy as np
from dataLibFarah import DataLib

def test_load_csv(tmp_path):
    # Create a sample CSV
    file = tmp_path / "test.csv"
    pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]}).to_csv(file, index=False)

    # Test loading CSV
    df = DataLib.load_csv(file)
    assert not df.empty
    assert list(df.columns) == ["col1", "col2"]

def test_save_csv(tmp_path):
    # Create a DataFrame
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    file = tmp_path / "test.csv"

    # Test saving CSV
    DataLib.save_csv(df, file)
    loaded_df = pd.read_csv(file)
    assert loaded_df.equals(df)

def test_normalize_data():
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    normalized = DataLib.normalize_data(df)
    assert normalized.min().min() == 0
    assert normalized.max().max() == 1

def test_handle_missing_values():
    df = pd.DataFrame({"col1": [1, np.nan, 3], "col2": [4, 5, np.nan]})
    filled = DataLib.handle_missing_values(df)
    assert not filled.isnull().any().any()

def test_calculate_statistics():
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    stats = DataLib.calculate_statistics(df)
    assert "mean" in stats.index

def test_mean():
    data = [1, 2, 3]
    assert DataLib.mean(data) == np.mean(data)

def test_median():
    data = [1, 2, 3]
    assert DataLib.median(data) == np.median(data)

def test_mode():
    data = pd.Series([1, 2, 2, 3])
    assert DataLib.mode(data) == 2

def test_standard_deviation():
    data = [1, 2, 3]
    assert DataLib.standard_deviation(data) == np.std(data)

def test_t_test():
    sample1 = [1, 2, 3]
    sample2 = [4, 5, 6]
    stat, p_value = DataLib.t_test(sample1, sample2)
    assert p_value < 1

def test_chi_squared_test():
    observed = [10, 20, 30]
    expected = [10, 20, 30]
    chi2, p_value, _ = DataLib.chi_squared_test(observed, expected)
    assert p_value > 0.05

def test_correlation_matrix():
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    correlation = DataLib.correlation_matrix(df)
    assert correlation is not None

def test_linear_regression():
    x = np.array([[1], [2], [3]])
    y = np.array([4, 5, 6])
    model, coef, intercept = DataLib.linear_regression(x, y)
    assert len(coef) == 1

def test_polynomial_regression():
    x = np.array([1, 2, 3]).reshape(-1, 1)
    y = np.array([4, 5, 6]).reshape(-1, 1)
    model, coef = DataLib.polynomial_regression(x, y, degree=2)
    assert len(coef) == 3

def test_apply_pca():
    data = np.random.rand(10, 5)
    transformed_data, explained_variance = DataLib.apply_pca(data)
    assert transformed_data.shape[1] == 2

def test_kmeans_clustering():
    data = np.random.rand(10, 2)
    clusters, centers = DataLib.kmeans_clustering(data, n_clusters=2)
    assert len(centers) == 2

def test_knn_classification():
    train_data = [[1], [2], [3]]
    train_labels = [0, 1, 1]
    test_data = [[1.5]]
    prediction = DataLib.knn_classification(train_data, train_labels, test_data)
    assert prediction[0] in [0, 1]

def test_decision_tree_classification():
    train_data = [[1], [2], [3]]
    train_labels = [0, 1, 1]
    test_data = [[1.5]]
    prediction = DataLib.decision_tree_classification(train_data, train_labels, test_data)
    assert prediction[0] in [0, 1]
