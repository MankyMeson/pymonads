import typing
import copy
import inspect


class Maybe:

    MAYBE_STATES = ["just", "nothing"]


    def __init__(self, value: typing.Any, maybe: str = "just") -> None:
        if mabye not in Maybe.MAYBE_STATES:
            raise RuntimeError("Given maybe state must be one of {}".format(MAYBE_STATES))

        self.maybe = maybe
        self.value = None
        if self.maybe == "just":
            self.value = value


    def __str__(self) -> str:
        if self.maybe == "nothing":
            return "nothing"
        return "just " + self.value


    def bind(self, function: typing.Callable) -> None:
        new_maybe: typing.Self = bind_maybe(self, function)
        self.value, self.maybe = new_maybe.value, new_maybe.maybe


    def is_just(self) -> bool:
        return self.maybe == "just"


    def is_nothing(self) -> bool:
        return self.maybe == "nothing"


    def fmap(self, function: typing.Callable) -> None:
        new_maybe: Maybe = fmap_maybe(self, function)
        self.value = new_maybe.value


def return_maybe(value: typing.Any) -> Maybe:
    return Maybe(value)


def bind_maybe(maybe: Maybe, function: typing.Callable) -> Maybe:
    fn_type_signature = typing.signature(function)
    return_t = fn_type_signature.return_annotation

    if (
        len(fn_type_signature.parameters) != 1 or
        ( return_t is not function_type_signature.empty and return_t != Maybe )
    ):
        raise TypeError(
            "Function passed to bind_maybe violates Monad laws, must take one argument and return a Maybe.\n"
            "The function's type signature is {}".format(str(function_type_signature))
        )

    maybe_val = copy.deepcopy(maybe.value)
    new_maybe: Maybe = function(record_val)

    if new_maybe.maybe == "nothing":
        new_val = None
    else:
        new_val = new_maybe.value

    return Maybe(
        value = new_val,
        maybe = new_maybe.maybe
    )


def fmap_maybe(maybe: Maybe, function: typing.Callable) -> Maybe:
    fn_type_signature = typing.signature(function)
    return_t: type = fn_type_signature.return_annotation

    if len(fn_type_signature.parameters) != 1:
        raise TypeError("placeholder")

    if maybe.is_just() :
        maybe_val: typing.Any = copy.deepcopy(maybe.value)
        new_maybe_val = function(maybe_val)
        return Maybe(new_maybe_val)
    elif maybe.is_nothing() :
        return Maybe(None, maybe = "nothing")

