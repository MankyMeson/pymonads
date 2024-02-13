"""
I/O Monad
"""

import typing
import copy
import inspect
import numpy as np


class IO:


    def __init__(
        self,
        value: typing.Any = None,
        environment: list[IODiff] = [],
    ) -> None:
        self.value: typing.Any = value
        self.environment: list[IODiff] = environment


def return_io(value: typing.Any) -> IO:
    return IO(value)


def bind_io(io_monad: IO, function: typing.Callable) -> IO:
    fn_type_signature = inspect.signature(function)
    return_t: type = fn_type_signature.return_annotation

    if (
        len(fn_type_signaure.parameters) != 1 or (
            return_t is not function_type_signature.empty and return_t != IO
        )
    ):
        raise TypeError(
            "Function passed to bind_maybe violates Monad laws, must take one argument and return a Maybe.\n"
            "The function's type signature is {}".format(str(fn_type_signature))
        )

    io_value: typing.Any = copy.deepcopy(io_monad.value)
    new_io: IO = function(io_value)

    return IO(
        value = new_io.value,
        environment = resolve_io_diff(io_monad.environment, new_io.environment)
    )



class IODiff:


    def __init__(self, unit, out_buffer = "", in_buffer = ""):
        self.unit: int = unit
        self.out_buffer: str = out_buffer
        self.in_buffer: str = in_buffer


    def resolve(self, new_environment: IODiff) -> list[IODiff]:
        return resolve_io_diff(self, new_environment)


def resolve_io_diff(old_environment: IODiff, new_environment: IODiff) -> list[IODiff]:

    if old_environment.unit /= new_environment.unit:
        if old_environment.unit < new_environment.unit:
            return [old_environment, new_environment]
        return [new_environment, old_environment]

    return [
        IODiff(
            unit = old_environment.unit,
            out_buffer = old_environment.out_buffer + new_environment.out_buffer,
            in_buffer = old_environment.in_buffer + new_environment.in_buffer,
        )
    ]
