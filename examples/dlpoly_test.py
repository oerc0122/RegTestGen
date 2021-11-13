import dlpoly
from RegTestGen.core.test_set import TestSet
from dlpoly_py_func import StatisFileParam, StatisReadWrap


# Using experimental test class
dlp_test = TestSet('dlp_test', {('dlpoly',), ('numpy',)})
dlp_test.add_test_class(dlpoly.statis.Statis, init_args=(), func='read',
                        param_types=(StatisFileParam(),), props=('data',), fail=False, groups=('cls',))

dlp_test.add_arg_to_group('cls', ('ones',), (27, 3), file='dlp_ones_cls.statis')


# Using function wrapper
dlp_test.add_requirement(('RegTestGen.examples.dlpoly_py_func', 'StatisReadWrap'))

dlp_test.add_test_function(StatisReadWrap, param_types=(StatisFileParam(),), fail=False, groups=('func',))

dlp_test.add_arg_to_group('func', ('ones',), (27, 3), file='dlp_ones_func.statis')

dlp_test.write('all', 'dlp_test.py')
