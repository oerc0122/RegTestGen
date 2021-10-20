import pickle
import pprint


class TestClass:
    """
    Object containing information about a class to test
    """


class TestFunc:
    """
    Object containing information about an function to test
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

        name = self.gen_name(types)

        return TestResult(name, self.func, params, results)

    def gen_name(self, types):
        types = "_".join(f"{type}_{cls.name}" for type, cls in zip(types, self.param_types))
        return (
            "test_"
            f"{self.func.__name__}_"
            f"{types}"
        )

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
    def __init__(self, name, func, params, results):
        self._name = ""
        self.name = name
        self._func = func
        self._params = params
        self._results = results

    tests = {}
    func = property(lambda self: self._func)
    params = property(lambda self: self._params)
    results = property(lambda self: self._results)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        """
        Append count to name
        """
        if self.name:
            print("Log: Cannot overwrite name - " + self.name)
            return
        count = TestResult.tests.get(value, 0) + 1
        TestResult.tests[value] = count
        if count > 1:
            self._name = value + f"_{count}"
        else:
            self._name = value

    def dump(self, file):
        """
        Dump as pickle object for simple tests
        """
        pickle.dump(self, file)

    def write(self, file, format):
        if format == 'pytest':
            self.write_pytest(file)
        else:
            print(f"Log: Cannot write to format {format}")

    def write_pytest(self, file):
        """
        Write as Pytest test
        Assumes open file
        """

        _writeln("", file=file)
        _writeln(f"def {self.name}():", file=file)
        if all(self.is_simple(param) for param in self.params):
            _writeln(f"params = {pprint.pformat(self.params)}", indent=1, file=file)
        else:
            with open(self.name+".inputdata", 'wb') as pickleFile:
                pickle.dump(self.params, pickleFile)
            _writeln(f"""with open({self.name+".inputdata"}, "rb") as pickleFile:""", indent=1, file=file)
            _writeln("params = pickle.load(pickleFile)", indent=2, file=file)

        if issubclass(type(self.results), BaseException): # Result is exception (expected)
            _writeln(f"pytest.raises({type(self.results).__name__}, {self.func.__name__}, *params)", indent=1, file=file)
            return

        if self.is_simple(self.results):
            _writeln(f"expected_results = {pprint.pformat(self.results)}", indent=1, file=file)
        else:
            with open(self.name+".resultdata", 'wb') as pickleFile:
                pickle.dump(self.results, pickleFile)

            _writeln(f"""with open({self.name+".resultdata"}, "rb") as pickleFile:""", indent=1, file=file)
            _writeln("expected_results = pickle.load(pickleFile)", indent=2, file=file)

        _writeln(f"results = {self.func.__name__}(*params)", indent=1, file=file)
        _writeln("assert results == expected_results", indent=1, file=file)
        _writeln("", file=file)

    @staticmethod
    def read(file):
        """
        Read pickle file
        """
        return pickle.load(file)

    @staticmethod
    def is_simple(obj):
        """
        Determine whether a file is simple enough to just be written into the test
        or whether it deserves dumping to a file.
        """
        return pprint.isreadable(obj) and len(pprint.pformat(obj)) < 80


def _writeln(*line, file=None, indent=0, **kwargs):
    file.write((" "*3*indent)+"".join(line)+'\n')


def write_all(test_set, file, **kwargs):
    with open(file, 'w') as outFile:
        # Write preamble
        _writeln("import pytest", file=outFile)
        _writeln("import pickle", file=outFile)
        for imp in kwargs.get('required_imports', []):
            # If importing whole module
            if not isinstance(imp, (list, tuple)):
                _writeln(f"import {imp}", file=outFile)
            # Alternative syntax
            elif len(imp) == 1:
                _writeln(f"import {imp[0]}", file=outFile)
            # Else importing components
            else:
                _writeln(f"from {imp[0]} import {', '.join(imp[1:])}", file=outFile)

        for test in test_set:
            test.write_pytest(outFile)
