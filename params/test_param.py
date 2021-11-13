from abc import ABC


class TestParam(ABC):
    def __init__(self, *args, limits=None, **kwargs):
        if limits is None:
            self.limits = [0, 1]
        else:
            self.limits = limits
        self.name = type(self).__name__

    @property
    def value(self):
        return self._value

    @property
    def limits(self):
        return self._limits

    @limits.setter
    def limits(self, new_limits):
        if len(new_limits) != 2:
            print('Error, invalid limits')
            return
        self._limits = new_limits

    def gen(self, type, *args, **kwargs):
        if hasattr(self, type):
            getattr(self, type)(*args, **kwargs)
        else:
            print("Log: {self.__name__} cannot generate type {type}.")

    @staticmethod
    def get_prefix_args(args: dict, prefix, **defaults):
        out = defaults
        for key, val in args.items():
            if key.startswith(prefix+'_'):
                new_key = key.replace(prefix+'_', '', 1)
                out[new_key] = val
        return out
