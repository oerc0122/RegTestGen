from RegTestGen.core.test_set import TestObj
from RegTestGen.examples.func import add_two_numbers
from RegTestGen.params.float_param import ScalarFloat, VectorFloat
from RegTestGen.params.fixed_param import FixedParam

test = TestObj(add_two_numbers, [ScalarFloat(), FixedParam(value=7.0)])
test.gen('fixed', 1, fixval=2.0)

test = TestObj(add_two_numbers, [ScalarFloat(), VectorFloat()], fail=True)
test.gen('seq', 3)

print(*test.params)
print(test.results)
