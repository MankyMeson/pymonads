import typing
import copy
import inspect


class Maybe:

    MAYBE_STATES = ["just", "nothing"]


    def __init__(self, value, maybe = "just"):
        if mabye not in Maybe.MAYBE_STATES:
            raise RuntimeError("Given maybe state must be one of {}".format(MAYBE_STATES))

        self.maybe = maybe
        self.value = None
        if self.maybe == "just":
            self.value = value


    def __str__(self):
        if self.maybe == "nothing":
            return "nothing"
        return "just " + self.value


    def bind(self, function: typing.Callable):
        new_record = bind_record(self, function)
        self.value, self.maybe = new_record.value, new_record.maybe


def return_maybe(value) -> Maybe:
    return Maybe(value)


def bind_maybe(maybe: Maybe, function: typing.Callable) -> Maybe:
    fn_type_signature = typing.signature(function)
    return_t = fn_type_signature.return_annotation

    if (
        len(fn_type_signature.parameters) != 1 or
        ( return_t is not function_type_signature.empty and return_t != )
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
