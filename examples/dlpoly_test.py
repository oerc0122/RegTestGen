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


for var_type in ('zeros', 'ones', 'rand', 'randflat'): #, 'seq', 'fixed'
    dlp_test.add_arg_to_group('func', (var_type,), (27, 3), file=f'dlp_{var_type}_func.statis', step_type='fixed', step_fixval=-1.0)

dlp_test.write('all', 'dlp_test.py')
