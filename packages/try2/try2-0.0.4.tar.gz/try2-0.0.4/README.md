
# try2
Simple wrapper for try-except blocks

# Installation
```
pip install try2
```

# Installation
```
pip install try2
```

# Quickstart
```python
from try2 import try2

def reciprocal(n):
    return 1 / n

ls = [1, 2, 0, 3, 0, 4]

for number in ls:
    x = try2(reciprocal, number, "bad")
    print(number, "=>", x)

# 1 => 1.0
# 2 => 0.5
# 0 => bad
# 3 => 0.3333333333333333
# 0 => bad
# 4 => 0.25

```

# Why I wrote this
I needed a simply one-liner try-except function for many of my projects, 
and I found myself defining helper try-except functions everywhere, which got annoying quickly

# But what if I need a more complex try-except wrapper?
If your wrapper gets any more complex than this, it's probably a good idea to write your own function
