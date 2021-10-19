from abc import ABC


class TestParam(ABC):
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
        if hasattr(self, type):
            getattr(self, type)(*args, **kwargs)
        else:
            print("Log: {self.__name__} cannot generate type {type}.")

    def get_prefix_args(args: dict, prefix):
        out = {}
        for key, val in args.values():
            if key.startswith(prefix+'_'):
                new_key = key.replace(prefix+'_', '', 1)
                out[new_key] = val
        return out
