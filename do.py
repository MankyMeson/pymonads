"""
Module defines do function to sequentially bind a list of functions to a monad
"""
import typing

import maybe
import record
import array
import io

monad_generic_t = (
    maybe.Maybe   |
    record.Record |
    array.List
)

def do(monad: monad_generic_t, function_list: list[typing.Callable]) -> monad_generic_t:
    for function in function_list:
        monad.bind(function)
