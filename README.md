# Pattern Utils
Pattern matching utilities.

Currently the only implemented matcher is for generators/iterators.

Example:
```python
from patternlib import generator as gen


def example_generator():
    yield "some resource"
    return "done"


match gen.matcher(example_generator()):
    case gen.Node(resource, gen.Empty(end_result)):
        print(resource, end_result)
```
