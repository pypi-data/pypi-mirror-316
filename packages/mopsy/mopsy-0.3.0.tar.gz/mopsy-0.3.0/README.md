[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
[![PyPI-Server](https://img.shields.io/pypi/v/mopsy.svg)](https://pypi.org/project/mopsy/)
![Unit tests](https://github.com/BiocPy/mopsy/actions/workflows/pypi-test.yml/badge.svg)

# mopsy - Matrix Operations in Python

Convenience library to perform row/column operations over numpy and scipy matrices. Provides an interface similar to base R matrix methods/MatrixStats methods in python.

## Installation

Install from [pypi](https://pypi.org/project/mopsy/)

```shell
pip install mopsy
```

## Usage

```python
from mopsy import colsum
import random from rd
# generate a random sparse array with some density
from scipy.sparse import random
mat = random(10, 150, 0.25)

# generate random groups
ngrps = 15
gsets = [x for x in range(15)]
groups = [rd.choice(gsets) for x in range(mat.shape[axis])]

colsum(mat, groups)
```

Methods are available to perform `sum`, `median`, `mean` along any axis. a generic `apply` method is also available for perform row-wise or column-wise operations.

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.1.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
