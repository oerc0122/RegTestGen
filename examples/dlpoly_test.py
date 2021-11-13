import dlpoly
from RegTestGen.core.test_set import TestSet
from dlpoly_py_func import StatisFileParam

dlp_test = TestSet('dlp_test', {('dlpoly',)})
dlp_test.add_test_class(dlpoly.statis.Statis, init_args=(), func='read',
                        param_types=(StatisFileParam(),), props=('data',), fail=False, groups=('dlpoly',))

dlp_test.add_arg_to_group('dlpoly', ('ones',), (27, 3), file='dlp_ones.statis')

dlp_test.write('all', 'dlp_test.py')
