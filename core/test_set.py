import pickle


class TestObj:
    """
    Object containing information about a test to run
    """
    def __init__(self, func, param_types, fail=False):
        self.func = func
        self.param_types = param_types
        self.fail = fail

    def gen(self, types, length, *args, **kwargs):
        """
        Generate test data
        """
        if not isinstance(types, (list, tuple)):
            types = [types for elem in self.param_types]

        for i, param in enumerate(self.param_types):
            param.gen(types[i], length, *args, **kwargs)

        params = [param.value for param in self.param_types]
        try:
            results = self.func(*params)
        except Exception as error:
            if self.fail:
                results = error
            else:
                print('Unexpected failure in test')
                raise error

        return TestResult(self.func, params, results)

    def test(self):
        """
        Test against the stored values
        """
        test_res = self.func(*self.params)
        return test_res == self.results


class TestResult:
    """
    Object containing dumpable test results
    """
    def __init__(self, func, params, results):
        self._func = func
        self._params = params
        self._results = results

    func = property(lambda self: self._func)
    params = property(lambda self: self._params)
    results = property(lambda self: self._results)

    def dump(self, file):
        """
        Dump as pickle object for simple tests
        """
        pickle.dump(self, file)

    def write(self, file):
        """
        Write as Pytest test
        """
        pass

    @staticmethod
    def read(file):
        """
        Read pickle file
        """
        return pickle.load(file)
