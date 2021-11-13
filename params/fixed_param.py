from .test_param import TestParam


class FixedParam(TestParam):
    def __init__(self, *args, **kwargs):
        TestParam.__init__(self, *args, **kwargs)
        self._value = kwargs['value']

    def gen(self, type, *args, **kwargs):
        return self.value
