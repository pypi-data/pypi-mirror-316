
# default_deepcopy
deepcopy, but if exception, return a default value

# Installation
```
pip install default_deepcopy
```

# Quickstart
```python

from inspect import currentframe
import collections.abc

from src.default_deepcopy import default_deepcopy

class Dog:
    pass

values = [
    12200,
    3.14159,
    "apple",
    True,
    None,
    [1, 2, 3],
    (4, 5, 6),
    {7, 8, 9},
    {"apple":2, "orange": 5},
    Dog(),
    currentframe(),
    collections.abc
]

for value in values:
    value_copied = default_deepcopy(value, "<BAD VALUE>")
    print(value, value_copied)

# 12200 12200
# 3.14159 3.14159
# apple apple
# True True
# None None
# [1, 2, 3] [1, 2, 3]
# (4, 5, 6) (4, 5, 6)
# {8, 9, 7} {8, 9, 7}
# {'apple': 2, 'orange': 5} {'apple': 2, 'orange': 5}
# <__main__.Dog object at 0x1026e7620> <__main__.Dog object at 0x1027c31d0>
# <frame at 0x1027...> <BAD VALUE>
# <module 'collections.abc' from ...> <BAD VALUE>
```

# Why I wrote this
Too many helper functions doing this, so I abstracted it into a library