# DataLib

[![Test](https://github.com/elayeboussama/oussama_datalib/actions/workflows/test.yml/badge.svg)](https://github.com/elayeboussama/oussama_datalib/actions/workflows/test.yml)

A simplified Python library for data manipulation, analysis, and machine learning.

## Features

- Data Processing: Loading, cleaning, and preprocessing functions
- Analysis: Linear regression, polynomial regression, and multiple regression
- Statistics: Basic statistical calculations
- Visualization: Various plotting functions using matplotlib and seaborn
- Machine Learning:
  - Supervised Learning: KNN, Decision Trees, Random Forests
  - Unsupervised Learning: K-means, PCA, Gaussian Mixture
  - Reinforcement Learning: Basic Q-Learning and SARSA

## Installation

You can install the package directly from PyPI:

```bash
pip install oussama-datalib
```
Or using Poetry:

```bash
poetry add oussama-datalib
```
 

## Usage

Here's a simple example of using DataLib:

```python
from src.datalib.data_processing import load_csv, fill_missing_values
from src.datalib.visualization import plot_histogram
import pandas as pd

# Load data
df = pd.read_csv('your_data.csv')

# Fill missing values
df = fill_missing_values(df, 'column_name', method='mean')

# Create visualization
plot_histogram(df, 'column_name')
```

For a complete example, check out `example/execution_example.py`. To run it:

```bash
poetry run python example/execution_example.py
```

## Testing

To run the tests:

```bash
poetry run pytest
```

## Documentation

To build the documentation:

```bash
poetry run sphinx-build -b html docs docs/build
```

Then open `docs/build/index.html` in your browser.

## Project Structure

```
datalib/
├── src/
│ └── datalib/
│     ├── init.py
│     ├── analysis.py
│     ├── data_processing.py
│     ├── reinforcement.py
│     ├── statistics.py
│     ├── supervised.py
│     ├── unsupervised.py
│     └── visualization.py
├── tests/
│   ├── conftest.py
│   ├── test_analysis.py
│   ├── test_data_processing.py
│   ├── test_reinforcement.py
│   ├── test_statistics.py
│   ├── test_supervised.py
│   ├── test_unsupervised.py
│   └── test_visualization.py
├── docs/
│   ├── conf.py
│   ├── index.rst
│   ├── modules.rst
│   └── build/
│   ├── html/
│   ├── doctrees/
│   └── static/
├── example/
│   └── execution_example.py
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
├── setup.py
└── .pre-commit-config.yaml
```

## Dependencies

- Python ≥ 3.10
- NumPy ≥ 1.21.0
- Pandas ≥ 2.2.3
- Matplotlib ≥ 3.4.0
- Seaborn ≥ 0.11.0
- Scikit-learn ≥ 1.0.0
- SciPy ≥ 1.7.0

## License

MIT License

## Author

Oussama ELAYEB (elayeb.oussama2020@gmail.com)

## Development Setup

1. Clone the repository
2. Install dependencies:
```bash
poetry install
```

3. Install pre-commit hooks:
```bash
poetry run pre-commit install
```

4. Run tests:
```bash
poetry run pytest
```

5. Run linting:
```bash
poetry run flake8
poetry run black .
poetry run isort .
```


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact

For questions, feedback, or support:
- Email: elayeb.oussama2020@gmail.com
- GitHub Issues: [Create an issue](https://github.com/elayeboussama/oussama_datalib/issues)

## Acknowledgments

- Thanks to the Python community for the amazing libraries that made this project possible
- Special thanks to all contributors who help improve this library
