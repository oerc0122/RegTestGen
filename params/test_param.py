class TestParam:
    def __init__(self, *args, limits=None, **kwargs):
        if limits is None:
            self.limits = [0, 1]
        else:
            self.limits = limits

    @property
    def value(self):
        return self.value_

    @property
    def limits(self):
        return self.limits_

    @limits.setter
    def limits(self, new_limits):
        if len(new_limits) != 2:
            print('Error, invalid limits')
            return
        self.limits_ = new_limits

    def gen(self, type, *args, **kwargs):
        if type == 'zeros':
            self.zeros(*args, **kwargs)
        elif type == 'ones':
            self.ones(*args, **kwargs)
        elif type == 'rand':
            self.rand(*args, **kwargs)
        elif type == 'flatrand':
            self.flatrand(*args, **kwargs)
        elif type == 'seq':
            self.seq(*args, **kwargs)
        elif type == 'seq':
            self.seq(*args, **kwargs)
        elif type == 'fixed':
            self.fixed(*args, **kwargs)

    def zeros(self, *args, **kwargs):
        raise NotImplementedError()

    def ones(self, *args, **kwargs):
        raise NotImplementedError()

    def rand(self, *args, **kwargs):
        raise NotImplementedError()

    def flatrand(self, *args, **kwargs):
        raise NotImplementedError()

    def seq(self, *args, **kwargs):
        raise NotImplementedError()

    def fixed(self, *args, **kwargs):
        raise NotImplementedError()
