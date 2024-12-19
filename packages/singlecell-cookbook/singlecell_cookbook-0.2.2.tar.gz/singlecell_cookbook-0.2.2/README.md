# singlecell-cookbook

[![Tests](https://github.com/argearriojas/singlecell-cookbook/actions/workflows/tests.yml/badge.svg)](https://github.com/argearriojas/singlecell-cookbook/actions/workflows/tests.yml)

A collection of tools for analyzing single-cell genomics data.

## Installation

You can install the package using pip:

```bash
pip install singlecell-cookbook
```

For development installation:

```bash
git clone https://github.com/argearriojas/singlecell-cookbook.git
cd singlecell-cookbook
pip install -e ".[dev]"
```

### R Dependencies

Some features (like pseudobulk analysis) require R and specific R packages. To use these features:

1. Install the required R packages in R:

```R
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install(c("edgeR", "MAST"))
```

2. Install the R dependencies in Python:

```bash
pip install "singlecell-cookbook[r]"
```

## Documentation

Documentation is available at [Read the Docs](https://singlecell-cookbook.readthedocs.io/).

## Development

To set up the development environment:

1. Clone the repository
2. Install development dependencies: `pip install -e ".[dev]"`
3. Install pre-commit hooks: `pre-commit install`

## License

TBD. We need to assess the license according to the imported packages.

## Author

Argenis Arriojas ([arriojasmaldonado001@umb.edu](mailto:arriojasmaldonado001@umb.edu))
