# Pattern Utils
[![PyPI version](https://badge.fury.io/py/pattern-utils.svg)](https://badge.fury.io/py/pattern-utils)

Pattern matching utilities.

Currently the only implemented matcher is for generators/iterators.

## Install
pip install pattern-utils

## Example
```python
from patternlib import generator as gen


def example_generator():
    yield "some resource"
    return "done"


match gen.matcher(example_generator()):
    case gen.Node(resource, gen.Empty(end_result)):
        print(resource, end_result)
```
