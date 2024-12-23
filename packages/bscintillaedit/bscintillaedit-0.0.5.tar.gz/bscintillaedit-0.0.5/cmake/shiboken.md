# shiboken.cmake

This script contains some helper cmake functions and macros.

## Using

In the top `CMakeLists.txt`:

```cmake
include(cmake/pretty_print.cmake)
include(cmake/pyside_config.cmake)
include(cmake/shiboken.cmake)
```

```cmake
find_shiboken()
```

This will create a couple of `SHIBOKEN_XXX` variables. You can use the helper `pretty_print_variables` to print all of them:

```cmake
pretty_print_variables(SHIBOKEN_)
```
