# DataLib

**DataLib** is a Python library designed to simplify data manipulation, analysis, and visualization. It provides tools for both basic and advanced users, enabling efficient handling of datasets, statistical computations, and machine learning tasks.

## Features

### Data Manipulation
- Load and save CSV files.
- Normalize data.
- Handle missing values.

### Statistical Calculations
- Compute mean, median, mode, and standard deviation.
- Perform statistical tests (t-test, chi-squared).

### Data Visualization
- Create scatter plots, bar charts, and histograms.
- Generate advanced visualizations like correlation matrices.

### Advanced Analysis
- Perform linear and polynomial regression.
- Apply PCA for dimensionality reduction.
- Use k-means clustering.
- Perform supervised classification (k-NN, decision trees).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/riahiFarah/DataLib.git
   ```

2. Navigate to the project directory:
   ```bash
   cd dataLibFarah
   ```

3. Install the library:
   ```bash
   pip install .
   ```

## Usage

### Example 1: Load and Save CSV
```python
from datalib import DataLib

df = DataLib.load_csv("data.csv")
DataLib.save_csv(df, "output.csv")
```

### Example 2: Normalize Data
```python
normalized_df = DataLib.normalize_data(df)
```

### Example 3: Perform Linear Regression
```python
x = [[1], [2], [3]]
y = [4, 5, 6]
model, coef, intercept = DataLib.linear_regression(x, y)
```

## Development

### Setting Up for Development
1. Install development dependencies:
   ```bash
   pip install .[dev]
   ```

2. Run tests:
   ```bash
   pytest tests/
   ```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request to discuss potential changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
