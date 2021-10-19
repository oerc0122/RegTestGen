from random import uniform
from .test_param import TestParam


class ScalarFloat(TestParam):
    """ Single scalar float value """
    def __init__(self, *args, **kwargs):
        TestParam.__init__(self, *args, **kwargs)

    def zeros(self, *args, **kwargs):
        self.value_ = 0.0

    def ones(self, *args, **kwargs):
        self.value_ = 1.0

    def rand(self, *args, **kwargs):
        self.value_ = uniform(*kwargs.get('limits', [0, 1]))

    def randflat(self, *args, **kwargs):
        self.value_ = uniform(*kwargs.get('limits', [0, 1]))

    def seq(self, *args, **kwargs):
        self.value_ = 0.0

    def fixed(self, *args, **kwargs):
        self.value_ = kwargs['fixval']


class VectorFloat(TestParam):
    """ Single vector float value """
    def __init__(self, *args, **kwargs):
        TestParam.__init__(self, *args, **kwargs)

    def zeros(self, length, *args, **kwargs):
        self.value_ = [0.0 for i in range(length)]

    def ones(self, length, *args, **kwargs):
        self.value_ = [1.0 for i in range(length)]

    def rand(self, length, *args, **kwargs):
        self.value_ = [uniform(*kwargs.get('limits', [0, 1])) for i in range(length)]

    def randflat(self, length, *args, **kwargs):
        tmp = uniform(*kwargs.get('limits', [0, 1]))
        self.value_ = [tmp for i in range(length)]

    def seq(self, length, *args, **kwargs):
        start = kwargs.get('start', 0)
        step = kwargs.get('step', 1)
        length = start + length
        self.value_ = [float(i) for i in range(start, length, step)]

    def fixed(self, length, *args, **kwargs):
        self.value_ = [kwargs['fixval'] for i in range(length)]


class ArrayFloat(TestParam):
    """ Single array float value """
    def __init__(self, *args, **kwargs):
        TestParam.__init__(self, *args, **kwargs)

    def zeros(self, length, *args, **kwargs):
        self.value_ = [[0.0 for i in range(length[0])] for j in range(length[1])]

    def ones(self, length, *args, **kwargs):
        self.value_ = [[1.0 for i in range(length[0])] for j in range(length[1])]

    def rand(self, length, *args, **kwargs):
        self.value_ = [[uniform(*kwargs.get('limits', [0, 1])) for i in range(length[0])] for j in range(length[1])]

    def randflat(self, length, *args, **kwargs):
        tmp = uniform(*kwargs.get('limits', [0, 1]))
        self.value_ = [[tmp for i in range(length[0])] for j in range(length[1])]

    def seq(self, length, *args, **kwargs):
        start = kwargs.get('start', 0)
        step = kwargs.get('step', 1)
        length = [a + b for a, b in (start, length)]

        self.value_ = [[float(i*j + i) for i in range(start[0], length[0], step[0])]
                       for j in range(start[1], length[1], step[1])]

    def fixed(self, length, *args, **kwargs):
        self.value_ = [[kwargs['fixval'] for i in range(length[0])] for j in range(length[1])]
