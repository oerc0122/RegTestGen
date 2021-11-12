from RegTestGen.core.test_obj import TestFunc
from RegTestGen.examples.func import add_two_numbers
from RegTestGen.params.float_param import ScalarFloat, VectorFloat
from RegTestGen.params.fixed_param import FixedParam
from RegTestGen.core.test_set import TestSet
from RegTestGen.core.test_set import write_all

# Old style, manual
# -----------------
results = []
tests = []

tests.append(TestFunc(add_two_numbers, [ScalarFloat(), FixedParam(value=7.0)]))
tests.append(TestFunc(add_two_numbers, [ScalarFloat(), VectorFloat()], fail=True))
# tests.append(TestFunc(StatisReadWrap, [VectorArray(length=[30,27])], test_prop=['data']))

for test in tests:
    results.append(test.gen('fixed', length=1, fixval=2.0))
    results.append(test.gen('seq', length=3))
    for var_type in ('zeros', 'ones', 'rand', 'randflat', 'seq', 'fixed'):
        results.append(test.gen(var_type, length=3, fixval=1.3))

write_all(results, 'test.py', required_imports=(('RegTestGen.examples.func', 'add_two_numbers'),))


# New style, compact, filterable
# ------------------------------

test_set = TestSet('main_tests', {(('RegTestGen.examples.func', 'add_two_numbers'),)})
test_set.add_test_function(add_two_numbers, [ScalarFloat(), FixedParam(value=7.0)], groups=('addNums',))
test_set.add_test_function(add_two_numbers, [ScalarFloat(), VectorFloat()], groups=('addNums', 'failures'))

test_set.add_arg_to_group('addNums', 'fixed', length=1, fixval=2.0)
test_set.add_arg_to_group('addNums', 'seq', length=3)
for var_type in ('zeros', 'ones', 'rand', 'randflat', 'seq', 'fixed'):
    test_set.add_arg_to_group('addNums', var_type, length=3, fixval=2.0)

test_set.write('all', 'test_two.py')
