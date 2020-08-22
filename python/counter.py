"""
Cria uma implementação similiar ao object Counter do modulo collections.
https://docs.python.org/3.8/library/collections.html#collections.Counter
"""

import sys

from typing import List, Tuple, Any
from collections.abc import MutableMapping
from collections.abc import Iterable

class Counter(MutableMapping):
    def __init__(self, *args, **kwargs):
        for arg in args+(kwargs,):
            iter(arg)
            self._set_counter(arg)

    def _set_counter(self, arg):
        if isinstance(arg, str):
            self._count_str(arg)
        
        if isinstance(arg, dict):
            self.__dict__.update(arg)
        
        if isinstance(arg, list):
            self._count_occurrences_list(arg)

    def _count_occurrences_list(self, lista: List[Any]) -> None:
        for i in lista:
            self.__dict__[i] = list.count(i)

    def _coun_large_strs(self, strs: str) -> None:
        end_slice = 100
        max_chunks = len(strs)/100

        for i in range(max_chunks, step=100):
            sliced_text = strs[i: end_slice]
            if sliced_text:
                # Qual é o criterio para a contagem de palavras? Espaços?? 
                pass
            end_slice += 100

    def _count_str(self, strs: str) -> None:
        if sys.getsizeof(strs) >= 1e+9:
            self._count_large_strs(strs)
            return

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
        return len(self.__dict__)

    def __setitem__(self, key: Any, value: Any):
        self.__dict__[key] = value

    def __repr__(self) -> str:
        return f'Counter({str(self.__dict__)})'

    def most_common(self, n: int = None) -> List[Tuple[Any, int]]:
        items = sorted(self.__dict__.items(), key=lambda element_pair: element_pair[1], reverse=True)
        if not n:
            return items
            
        return items[:n]

    def elements(self) -> Any:
        for key, ocurrences in self.__dict__.items():
            for i in range(ocurrences):
                yield key

