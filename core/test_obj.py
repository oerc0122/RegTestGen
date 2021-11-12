from abc import ABC
from .test_result import TestResult


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
        self.func = func
        self.param_types = param_types
        self.props = props
        self.fail = fail

    def gen(self, types, length, *args, **kwargs):
        """
        Generate test data
        """
        args = self.gen_params(types, length, *args, **kwargs)
        instance = self.cls(*args)

        if self.func is not None:
            try:
                params = self.gen_params(types, length, *args, **kwargs)
                getattr(instance, self.func)(*params)

            except Exception as error:
                if self.fail:
                    results = error
                else:
                    print('Unexpected failure in test')
                    raise error

        results = [getattr(instance, prop) for prop in self.props]

        name = self.gen_name(types)
        return TestResult(name, self.func, params, results)

    @staticmethod
    def gen_method(cls, method, method_args, types, length, *args, **kwargs):
        """
        Run method
        """
        params = self.gen_params(types, length, *args, **kwargs)

        try:
            results = self.func(*params)
        except Exception as error:
            if self.fail:
                results = error
            else:
                print('Unexpected failure in test')
                raise error


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

        return TestResult(name, self.func, params, results)
