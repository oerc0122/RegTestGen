from RegTestGen.core.test_set import TestObj
from RegTestGen.examples.func import add_two_numbers
from RegTestGen.params.float_param import ScalarFloat, VectorFloat
from RegTestGen.params.fixed_param import FixedParam

results = []
tests = []

tests.append(TestObj(add_two_numbers, [ScalarFloat(), FixedParam(value=7.0)]))
tests.append(TestObj(add_two_numbers, [ScalarFloat(), VectorFloat()], fail=True))

for test in tests:
    results.append(test.gen('fixed', length=1, fixval=2.0))
    results.append(test.gen('seq', length=3))
    for var_type in ('zeros', 'ones', 'rand', 'randflat', 'seq', 'fixed'):
        results.append(test.gen(var_type, length=3, fixval=1.3))

for result in results:
    print(*result.params)
    print(result.results)
