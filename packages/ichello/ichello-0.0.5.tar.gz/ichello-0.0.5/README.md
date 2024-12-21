# ichello

This is a 'hello world' Python wrapped C++ app to show a sample packaging approach. It is based on the [Reference Nanobind Example](https://github.com/wjakob/nanobind_example) but will diverge over time.

It uses:

* `nanobind` to do the wrapping, defined in `src/binding.cpp`, 
* `CMake` to build the module shared library, defined in `CMakeLists.txt`
* `scikit-build-core` to interface the Python project definition in `pyproject.toml` and CMake.
* `cibuildwheel` to build wheels for various platforms using the CI.

To locally install and use the package you can do:

``` shell
pip install -e .
```

from the project directory.

Then you can do:

``` python
import ichello
ichello.get_sum([1.0, 2.0, 3.0])
>> 6.0
```

in a shell. The `get_sum` function is an instantiation of the template defined in `include.hpp` for the `double` type.



