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

- Minimal user effort should be required to make it more convenient than writing tests manually (and to avoid having to write "proper" documentation [minimum email criterion])
- The output tests should be "sensibly named"
- Tests should be able to be (re)generated multiple times
- Large (or unrecognised [non-core] Python object) results may be dumped as Pickle (alternatives?) objects and loaded for comparison in the testing.

## Current State

- Simply generates a "TestResult" whose results can be examined. Cannot dump yet.
- Generates floats (scalar/N-vector) for signature.
- Captures "failures" and compares exceptions.
