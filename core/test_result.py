import pickle
import pprint

from .utility import writeln


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

    def dump(self, filename):
        """
        Dump as pickle object for simple tests
        """
        pickle.dump(self, filename)

    def write(self, filename, format):
        if format == 'pytest':
            self.write_pytest(filename)
        else:
            print(f"Log: Cannot write to format {format}")

    def write_pytest(self, filename):
        """
        Write as Pytest test
        Assumes open file
        """

        writeln("", file=filename)
        writeln(f"def {self.name}():", file=filename)
        if all(self.is_simple(param) for param in self.params):
            writeln(f"params = {pprint.pformat(self.params)}", indent=1, file=filename)
        else:
            with open(self.name+".inputdata", 'wb') as pickleFile:
                pickle.dump(self.params, pickleFile)
            writeln(f"""with open({self.name+".inputdata"}, "rb") as pickleFile:""", indent=1, file=filename)
            writeln("params = pickle.load(pickleFile)", indent=2, file=filename)

        if issubclass(type(self.results), BaseException): # Result is exception (expected)
            writeln(f"pytest.raises({type(self.results).__name__}, {self.func.__name__}, *params)", indent=1, file=filename)
            return

        if self.is_simple(self.results):
            writeln(f"expected_results = {pprint.pformat(self.results)}", indent=1, file=filename)
        else:
            with open(self.name+".resultdata", 'wb') as pickleFile:
                pickle.dump(self.results, pickleFile)

            writeln(f"""with open({self.name+".resultdata"}, "rb") as pickleFile:""", indent=1, file=filename)
            writeln("expected_results = pickle.load(pickleFile)", indent=2, file=filename)

        writeln(f"results = {self.func.__name__}(*params)", indent=1, file=filename)
        writeln("assert results == expected_results", indent=1, file=filename)
        writeln("", file=filename)

    @staticmethod
    def read(filename):
        """
        Read pickle file
        """
        return pickle.load(filename)

    @staticmethod
    def is_simple(obj):
        """
        Determine whether a file is simple enough to just be written into the test
        or whether it deserves dumping to a file.
        """
        return pprint.isreadable(obj) and len(pprint.pformat(obj)) < 80
