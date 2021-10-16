import pickle


class TestObj:
    """
    Object containing information about a test to be dumped
    """
    def __init__(self, func, param_types, results=None, fail=False):
        self.func = func
        self.param_types = param_types
        self.results = results
        self.fail = fail

    def gen(self, types, length, *args, **kwargs):
        """
        Generate test data
        """
        if not isinstance(types, (list, tuple)):
            types = [types for elem in self.param_types]

        for i, param in enumerate(self.param_types):
            param.gen(types[i], length, *args, **kwargs)
        self.params = [param.value for param in self.param_types]
        try:
            self.results = self.func(*self.params)
        except:
            if self.fail:
                self.results = True
            else:
                raise NotImplementedError()

    def test(self):
        """
        Test against the stored values
        """
        test_res = self.func(*self.params)
        return test_res == self.results

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
