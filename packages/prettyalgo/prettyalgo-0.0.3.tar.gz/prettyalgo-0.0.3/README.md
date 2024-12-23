[![CircleCI](https://dl.circleci.com/status-badge/img/gh/adamhadani/prettyalgo/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/adamhadani/prettyalgo/tree/main)

# :sparkles: prettyalgo

Pretty print for programming puzzles.

Highlights:

* Pretty print data structures and algorithms, especially sequence-oriented ones involving arrays such as lists, tuples and strs, and iterations, in the vein of leetcode and similar programming puzzles.
* Extensive configurability for various display styles and usage modes, such as console-interactive, animated, and more.
* Extensive use of [pre-commit](https://https://pre-commit.com/) hooks and unit-tests coverage to ensure correct functionality. Programming puzzles are hard enough to solve and debug, we shouldn't make it more error-prone by trying to use this library!


## Getting Started

To install from PyPI, use pip:

    pip install prettyalgo


See the [examples](./examples) sub-directory for examples showing the usage of the library.

Typical output when using on the terminal in interactive mode would like:

```
Remove Duplicates From Sorted Array 2
-------------------------------------
len(lst):          9
i                  6
j                  4
count              4

+-----------------------------------------------------------------------------------------+
|         |         |         |         |         |         |         |         |         |
|    0    |    0    |    1    |    1    |    1    |    1    |    2    |    3    |    3    |
|         |         |         |         |         |         |         |         |         |
+-----------------------------------------------------------------------------------------+
                                                                 ^ i=6
                                             ^ j=4

Press Enter to continue...
```
