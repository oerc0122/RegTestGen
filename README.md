# RegTestGen

Code to automate process of writing regression tests in Python.

**N.B.** These are regression tests, not correctness tests.

## Idea

- The general idea is that a simple script (`<root>/examples/instr.py`) can be used to generate a whole suite of tests of different forms just via a set of function signatures.
- The User can define custom classes in order to handle function arguments specific to their problem (see: `<root>/params`).
- Testable functions are any functions accessible in Python which return values.
- In principle, the idea will be to allow the dumping of said tests in `pytest` (or other) format for directly importing into test suites.
- It may be possible to use this generator as the testing engine itself, however, that is unwise as many better testing engines exist with formats whose generation might be easily automated.
  Ideally these formats (e.g. `pytest`, `doctest`, `cucumber`) might be extensible/importable and easy to include by the User to suit needs.

## Software Requirements

- Minimal user effort should be required to make it more convenient than writing tests manually (and to avoid having to write "proper" documentation \[minimum email criterion\])
- Multiple tests/file and multiple files should be supported
- Tests should be able to be (re)generated multiple times
- Large (or unrecognised \[non-core\] Python object) results may be dumped as Pickle (alternatives?) objects and loaded for comparison in the testing.

## Current State

- Simply generates a `TestResult` whose results can be examined and dumped as pytest files.
- Generates floats (scalar/N-vector/NxM-array) for signature.
- Captures "failures" and compares exceptions.
- Several different modes of test generation (defined by class, in principle unlimited and extensible, fixable \[as in possible to be locked in signature\]). Currently support: zeros, ones, sequence (0,1,2...N), fixed value, random (specifiable limits), flat random (one random number repeated to fill array). Should cover most bases.
- The output tests are "sensibly named".
- Tests can be dumped as pytest files which run. 
- Used `pprint` to determine recoverable, reasonably sized data.
