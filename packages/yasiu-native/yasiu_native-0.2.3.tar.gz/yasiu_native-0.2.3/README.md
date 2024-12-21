# Readme of `yasiu-native`


## Installation

```shell
pip install yasiu-native
```
## Contains

Module has plenty useful decorators.

 - Flexible decorators
 - Time decorators

## Flexible decorator

Decorator for parametrizing decorators.

Turns single level decorator into two leveled decorator,
by passing decoration parameters alongside function signature for ease of use.

Decorators wrapped with `Flexible` can be used both with `()` and without `()` operator.

### Example with one level parametrized decorator.
```python
from yasiu_native.decorators import flexible_decorator


@flexible_decorator
def custom_decorator(func, decorParam):
    def wrapper(*a, **kw):
        print(f"Decoration Paramter is {decorParam}")
        return func(*a, **kw)

    return wrapper

@custom_decorator
def test_1():
    pass

@custom_decorator()
def test_2():
    pass

@custom_decorator(1)
def test_3(b=0):
    pass

@custom_decorator(decorParamA=1, decorParamB=2)
def test_3(b=0):
    pass

```
### Example with 2 level decorator
```python
from yasiu_native.decorators import flexible_decorator_2d

@flexible_decorator_2d
def custom_decorator(*posParam, **keyParam):
    "posParam: [Optional] positional argument for customizng your decorator behaviour"
    "keyParam: [Optional] keyword argument for customizng your decorator behaviour"

    def wrapper(decoratedFunction):
        "decoratedFunction: function To be decorated with your decorator."

        def inner(*args, **kwargs):
            "args kwargs: arguments of decorated funciton"
            "Use decorative arguments to modify decorator"

            ret = decoratedFunction(*args, **kwargs)
            return ret
        return inner
    return wrapper
```

## Time decorators

Decorators for measuring time with formatter.

- **measure_perf_time_decorator**

  decorator that measures function execution time using *time.perf_counter*


- **measure_real_time_decorator**

  decorator that measures function execution time using *time.time*

#### Measuring time

```py
from yasiu_native.time import measure_perf_time_decorator


@measure_perf_time_decorator()
def func():
    ...


@measure_perf_time_decorator(">4.1f")
def func():
    ...


@measure_perf_time_decorator(fmt=">4.1f")
def func():
    ...

"Example output:" # Function <name> executed in 3min
"Example output:" # Function <name> executed in 40.2s
"Example output:" # Function <name> executed in 10.2ms
```

#### Print buffering will impact your performance!

- Use with caution for multiple function calls


## Console execution timer

not here yet.

# All packages

[1. Native Package](https://pypi.org/project/yasiu-native/)

[2. Math Package](https://pypi.org/project/yasiu-math/)

[3. Image Package](https://pypi.org/project/yasiu-image/)

[4. Pyplot visualisation Package](https://pypi.org/project/yasiu-vis/)

