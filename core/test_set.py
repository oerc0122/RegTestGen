import itertools
from collections import defaultdict

from .test_obj import TestFunc, TestClass
from .utility import writeln


class TestSet:
    """
    A set of tests to manipulate as a group.
    """
    def __init__(self, name, requirements=set()):
        self.name = name
        self.requirements = requirements
        self._funcs = []
        self._classes = []
        self._tests = []
        self._lookup = defaultdict(list)
        self._args = defaultdict(list)
        self._func_groups = defaultdict(list)
        self._class_groups = defaultdict(list)

    funcs = property(lambda self: self._funcs)
    tests = property(lambda self: self._tests)
    lookup = property(lambda self: self._lookup)
    args = property(lambda self: self._args)
    func_groups = property(lambda self: self._func_groups)

    @property
    def groups(self):
        return self.list_groups()

    def list_groups(self, func=None):
        if func is not None:
            return self.lookup[func]
        return [group for group in self.func_groups]

    def add_requirement(self, module, *imports):
        self.requirements.add(tuple(module, *imports))

    def add_test_function(self, func, param_types, fail=False, ID=None, groups=()):
        if ID is None:
            ID = func.__name__
        if not isinstance(param_types, tuple):
            param_types = tuple(param_types)

        new = TestFunc(func, param_types, fail)
        self._funcs.append(new)
        self._add_func_to_group('all', new)
        self._add_func_to_group('funcs', new)
        self._add_func_to_group(ID, new)
        for group in groups:
            self._add_func_to_group(group, new)

    def add_test_class(self, cls, init_args, func, param_types, props, fail=False, ID=None, groups=()):
        if ID is None:
            ID = cls.__name__

        new = TestClass(cls, init_args, func, param_types, props, fail=False)
        self._classes.append(new)
        self._add_class_to_group('all', new)
        self._add_class_to_group('classes', new)
        self._add_class_to_group(ID, new)
        for group in groups:
            self._add_class_to_group(group, new)

    def add_arg_to_group(self, group, types, length, *args, **kwargs):
        params = (types, length, args, kwargs)
        self._args[group].append(params)

    def _add_func_to_group(self, group, func):
        self._func_groups[group].append(func)
        self._lookup[func].append(group)

    def _add_class_to_group(self, group, cls):
        self._class_groups[group].append(cls)
        self._lookup[cls].append(group)

    def clear_gen(self, group):
        self._args[group] = defaultdict(list)

    def write(self, group, filename, **kwargs):
        print(f"Writing {group} to {filename}")

        with open(filename, 'w') as outFile:
            # Write preamble
            writeln("import pytest", file=outFile)
            writeln("import pickle", file=outFile)
            for imp in itertools.chain(self.requirements, kwargs.get('required_imports', ())):
                # If importing whole module
                if not isinstance(imp, (list, tuple)):
                    writeln(f"import {imp}", file=outFile)
                # Alternative syntax
                elif len(imp) == 1:
                    writeln(f"import {imp[0]}", file=outFile)
                # Else importing components
                else:
                    writeln(f"from {imp[0]} import {', '.join(imp[1:])}", file=outFile)

            for result in self.gen_iter(group):
                result.write_pytest(outFile)

    def gen_iter(self, group):
        for func in self._func_groups[group]:
            args_to_test = set()
            for local_group in self.lookup[func]:
                for args in self._args[local_group]:
                    args = self._tuplise(args)
                    args_to_test.add(args)

            for args in args_to_test:
                types, length, args, kwargs = _from_tuple(args)
                result = func.gen(types, length, *args, **kwargs)
                yield result

        for cls in self._class_groups[group]:
            args_to_test = set()
            for local_group in self.lookup[cls]:
                for args in self._args[local_group]:
                    args = self._tuplise(args)
                    args_to_test.add(args)

            for args in args_to_test:
                types, length, args, kwargs = _from_tuple(args)
                result = cls.gen(types, length, *args, **kwargs)
                yield result

    def gen(self, group):
        return [result for result in self.gen_iter(group)]

    @staticmethod
    def _tuplise(args):
        tupargs = _to_tuple(args[2])
        tupkwargs = _to_tuple((args[3],))[0]

        return (args[0], args[1], tupargs, tupkwargs)


def write_all(test_set, filename, **kwargs):
    with open(filename, 'w') as outFile:
        # Write preamble
        writeln("import pytest", file=outFile)
        writeln("import pickle", file=outFile)
        for imp in kwargs.get('required_imports', []):
            # If importing whole module
            if not isinstance(imp, (list, tuple)):
                writeln(f"import {imp}", file=outFile)
            # Alternative syntax
            elif len(imp) == 1:
                writeln(f"import {imp[0]}", file=outFile)
            # Else importing components
            else:
                writeln(f"from {imp[0]} import {', '.join(imp[1:])}", file=outFile)

        for test in test_set:
            test.write_pytest(outFile)


def _to_tuple(args):
    proc_args = []
    for arg in args:
        if isinstance(arg, list):
            proc_args.append(("_:list", _to_tuple(arg)))
        elif isinstance(arg, tuple):
            proc_args.append(("_:tuple", _to_tuple(arg)))
        elif isinstance(arg, dict):
            proc_args.append(("_:dict", _to_tuple(arg.items())))
        else:
            proc_args.append(arg)

    if not isinstance(proc_args, tuple):
        proc_args = tuple(proc_args)

    return proc_args


def _from_tuple(args):
    outArgs = []
    for arg in args:
        if arg and isinstance(arg, tuple):
            if arg[0] == '_:dict':
                outArgs.append({key: val for key, val in _from_tuple(arg[1:][0])})
            elif arg[0] == '_:list':
                outArgs.append([val for val in _from_tuple(arg[1:])[0]])
            elif arg[0] == '_:tuple':
                outArgs.append(tuple(_from_tuple(arg[1:]))[0])
            else:
                outArgs.append(arg)
        else:
            outArgs.append(arg)

    return outArgs
