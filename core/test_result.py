import pickle
import pprint
from abc import ABC

from .utility import writeln


class TestResult(ABC):
    """
    Object containing dumpable test results
    """
    def __init__(self, name):
        self._name = ""
        self.name = name

    tests = {}

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
        raise NotImplementedError()

    def write_prop(self, test_filename, store_filename, par_name, par_data, curr_indent=0):

        print(par_name)
        try:
            simple = all(self.is_simple(param) for param in par_data)
        except TypeError:
            simple = self.is_simple(par_data)

        if simple:
            writeln(f"{par_name} = {pprint.pformat(par_data)}", indent=curr_indent+1, file=test_filename)
        else:
            with open(store_filename, 'wb') as pickleFile:
                pickle.dump(par_data, pickleFile)
            writeln(f"""with open("{store_filename}", "rb") as pickleFile:""", indent=curr_indent+1, file=test_filename)
            writeln(f"{par_name} = pickle.load(pickleFile)", indent=curr_indent+2, file=test_filename)

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
