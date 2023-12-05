# cppfug

Utilities for C++ project management.

## Requirements

- [CMake] >= 3.11
- [Git]

[CMake]: https://www.cmake.org
[Git]: https://git-scm.com/

## Commands

- `cppfug new`: Initializes new project. Currently only one project template
  exists which is meant to be used for header only libraries.
- `cppfug configure`: Runs CMake configuration on the project.
- `cppfug build`: Builds the project.
- `cppfug test`: Runs test cases.
- `cppfug clean`: Cleans all build files.