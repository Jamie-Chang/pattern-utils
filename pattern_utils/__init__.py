"""`patternlib` is a toolkit for pattern matching.

That's the intention anyway, the first and only matcher provided here is for 
generators, allowing peeking into the head elements of a generator.

Example::
```python
>>> from pattern_utils import generator as gen

>>> def example_generator():
...     yield "some resource"
...     return "done"

>>> match gen.matcher(example_generator()):
...     case gen.Node(resource, gen.Empty(end_result)):
...         print(resource, end_result)
some resource done
"""