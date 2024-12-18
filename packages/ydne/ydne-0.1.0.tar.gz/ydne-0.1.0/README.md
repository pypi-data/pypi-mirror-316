# Ydne - Data Science Utilities

## Overview

Ydne is a Python library containing a collection of data science utilities to streamline data preprocessing, analysis, and visualization.

## Features

- Data Cleaning
- Outlier Detection
- Feature Scaling
- Missing Value Handling
- Correlation Visualization
- Distribution Plotting

## Installation

```bash
pip install ydne
```

## Usage Examples


### Preprocessing
```python
from ydne.preprocessing import DataPreprocessor

# Scale features
scaled_features = DataPreprocessor.scale_features(X, method='standard')

# Handle missing values
processed_df = DataPreprocessor.handle_missing_values(your_dataframe)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
