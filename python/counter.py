
from collections.abc import MutableMapping
from collections.abc import Iterable

class Counter(MutableMapping):
    def __init__(self, *args, **kwargs):
        for arg in args+(kwargs,):
            self._set_counter(arg)

    def _set_counter(self, arg):
        if isinstance(arg, str):
            self.count_str(arg)
        
        if isinstance(arg, dict):
            self.__dict__.update(arg)
        
        if isinstance(arg, list):
            count_occurrences_list(arg)

    def _count_occurrences_list(self, lista):
        for i in lista:
            self.__dict__[i] = list.count(i)

    def _count_str(self, strs):
        splited_letters = [letter for letter in strs]
        for i in splited_letters:
            self.__dict__[i] = strs.count(i)

    def __delitem__(self):
        pass

    def __getitem__(self, key):
        return self.__dict__.get(key, 0)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        pass

    def __setitem__(self):
        pass

    def __repr__(self):
        return f'Counter({str(self.__dict__)})'

    def most_common(self):
        pass

    def elements(self):
        for key, ocurrences in self.__dict__.items():
            for i in range(ocurrences):
                yield key

