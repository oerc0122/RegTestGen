from abc import ABC

from .test_result import TestResult
from .utility import writeln
import sys


class TestBase(ABC):
    """
    Base class for test types
    """
    def __init__(self):
        pass

    def gen_params(self, types, length, *args, **kwargs):

        if not isinstance(types, (list, tuple)):
            types = [types for elem in self.param_types]

        for i, param in enumerate(self.param_types):
            param.gen(types[i], length, *args, **kwargs)

        params = [param.value for param in self.param_types]
        return params

    def gen_name(self, types):
        types = "_".join(f"{type}_{cls.name}" for type, cls in zip(types, self.param_types))
        return f"test_{self.func.__name__}_{types}"


class TestClass(TestBase):
    """
    Object containing information about a class to test
    """
    def __init__(self, cls, init_args, func, param_types, props, fail=False):
        self.cls = cls
        self.init_args = init_args
        if isinstance(func, str):
            self.func = getattr(cls, func)
        else:
            self.func = func
        self.param_types = param_types
        self.props = props
        self.fail = fail

    def gen(self, types, length, *args, **kwargs):
        """
        Generate test data
        """

        args = self.gen_params(types, length, *args, **kwargs)
        initialise = (*self.init_args,)
        instance = self.cls(*initialise)

        if self.func is not None:
            try:
                params = self.gen_params(types, length, *args, **kwargs)
                self.func(instance, *params)
                results = [getattr(instance, prop) for prop in self.props]

            except Exception as error:
                if self.fail:
                    results = error
                else:
                    print('Unexpected failure in test')
                    raise error

        name = self.gen_name(types)
        name = name.split('_')
        name.insert(1, self.cls.__name__)
        name = '_'.join(name)

        return self.TestClassResult(name, self.cls, initialise, self.func, self.props, params, results)

    class TestClassResult(TestResult):
        def __init__(self, name, cls, init_args, func, props, params, results):
            TestResult.__init__(self, name)
            self.cls = cls
            self.init_args = init_args
            self.props = props
            self.func = func
            self.params = params
            self.results = results

        def write_pytest(self, filename):
            """
            Write as Pytest test
            Assumes open file
            """

            writeln("", file=filename)
            writeln(f"def {self.name}():", file=filename)

            self.save_prop(filename, self.name+".initdata", "init_args", self.init_args)
            writeln(f"instance = {self.cls.__module__}.{self.cls.__name__}(*init_args)", indent=1, file=filename)

            self.save_prop(filename, self.name+".inputdata", "params", self.params)
            writeln(f"instance.{self.func.__name__}(*params)", indent=1, file=filename)

            if issubclass(type(self.results), BaseException): # Result is exception (expected)
                writeln(f"pytest.raises({type(self.results).__name__}, {self.func.__name__}, *params)", indent=1, file=filename)
                return

            self.save_prop(filename, self.name+".resultdata", "expected_results", self.results)

            for i, prop in enumerate(self.props):
                writeln(f"results = getattr(instance, '{prop}')", indent=2, file=filename)

                if "numpy" in sys.modules:
                    import numpy
                    if isinstance(self.results[i], numpy.ndarray):
                        writeln(f"numpy.array_equal(results, expected_results[{i}])", indent=2, file=filename)
                    else:
                        writeln(f"assert results == expected_results[{i}]", indent=2, file=filename)
                else:
                    writeln(f"assert results == expected_results[{i}]", indent=2, file=filename)


            writeln("", file=filename)


class TestFunc(TestBase):
    """
    Object containing information about an function to test
    """
    def __init__(self, func, param_types, fail=True):
        self.func = func
        self.param_types = param_types
        # We assume at point of running code is working as expected
        self.fail = fail

    def gen(self, types, length, *args, **kwargs):
        """
        Generate test data
        """
        params = self.gen_params(types, length, *args, **kwargs)

        try:
            results = self.func(*params)
        except Exception as error:
            if self.fail or kwargs.get('fail', True):
                results = error
            else:
                print('Unexpected failure in test')
                raise error

        name = self.gen_name(types)

        return self.TestFuncResult(name, self.func, params, results)

    class TestFuncResult(TestResult):
        def __init__(self, name, func, params, results):
            TestResult.__init__(self, name)
            self.func = func
            self.params = params
            self.results = results

        def write_pytest(self, filename):
            """
            Write as Pytest test
            Assumes open file
            """

            writeln("", file=filename)
            writeln(f"def {self.name}():", file=filename)

            self.save_prop(filename, self.name+".inputdata", "params", self.params)

            if issubclass(type(self.results), BaseException): # Result is exception (expected)
                writeln(f"pytest.raises({type(self.results).__name__}, {self.func.__name__}, *params)", indent=1, file=filename)
                return

            self.save_prop(filename, self.name+".resultdata", "expected_results", self.results)

            writeln(f"results = {self.func.__name__}(*params)", indent=1, file=filename)

            if 'numpy' in sys.modules:
                import numpy
                if isinstance(self.results, numpy.ndarray):
                    writeln('numpy.array_equal(results, expected_results)', indent=1, file=filename)
                else:
                    writeln("assert results == expected_results", indent=1, file=filename)
            else:
                writeln("assert results == expected_results", indent=1, file=filename)

            writeln("", file=filename)
