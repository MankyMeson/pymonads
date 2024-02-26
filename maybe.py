import typing
import copy
import inspect


class Maybe:
    """Maybe monad to represent failure states functionally.

    Maybe is a well used monad which can carry failure states from between operations, the failure state is denoted as \"nothing\"
    and the value is overwritten with None. The success state is denoted by \"just\" whereupon the value will remain available
    for use in future binds.

    Attributes:
        MAYBE_STATES (list[str]): A constant array containing the two strings, \"just\" and \"nothing\".
        maybe (str): The current failure state, can only be one of the aforementioned strings.
        value (typing.Any): The value contained by the monad, not of a fixed type.
    """

    MAYBE_STATES = ["just", "nothing"]


    def __init__(self, value: typing.Any, maybe: str = "just") -> None:
        """Initialisation fuction for Maybe.

        Args:
            value (typing.Any): The input value to be contained by the monad.
            maybe (str): The string to be used to represent state, must be one of MAYBE_STATES.
        Raises:
            RuntimeError: Incorrect state string given to the program.
        """
        if mabye not in Maybe.MAYBE_STATES:
            raise RuntimeError("Given maybe state must be one of {}".format(", ".join(MAYBE_STATES)))

        self.maybe: str = maybe
        self.value: typing.Any = None
        if self.maybe == "just":
            self.value: typing.Any = value


    def __str__(self) -> str:
        """Returns a string representation of the monad.

        Returns:
            (str) either \"nothing\" or \"just <value>\" where <value> is whatever is contained by the monad at the time of use.
        """
        if self.is_nothing():
            return "nothing"
        return "just " + self.value


    def bind(self, function: typing.Callable) -> None:
        """Modifies the monad according to a function given.

        Binding is one of the defining features of a monad, in essence, a function is applied to the value contained by the monad
        and the state of the monad is updated. This function has strict typing rules detailed below.

        Args:
            function (typing.Callable): the function to be binded, which must take a single value of the same type as self.value
                                        and return a Maybe monad.
        """
        new_maybe: typing.Self = bind_maybe(self, function)
        self.value, self.maybe = new_maybe.value, new_maybe.maybe


    def is_just(self) -> bool:
        """Returns True if just.

        Returns:
            (bool) True if the Maybe monad is in the successful state, i.e. \"just\" and false otherwise.
        """
        return self.maybe == "just"


    def is_nothing(self) -> bool:
        """Returns true if nothing.

        Returns:
            (bool) True if the Maybe monad is in the failure state, i.e. \"nothing\" and false otherwise.
        """
        return self.maybe == "nothing"


    def fmap(self, function: typing.Callable) -> None:
        """Maps a function onto the monad's value.

        Args:
            function (typing.Callable): A function which takes a value of the same type as self.value and returns a single value of any other type.
        """
        new_maybe: Maybe = fmap_maybe(self, function)
        self.value: typing.Any = new_maybe.value


def return_maybe(value: typing.Any) -> Maybe:
    """Returns a value wrapped in a Maybe monad.

    Return is the unit function in the set of functions applied to the monad by the bind operation. It is required for the
    definition of the rest of the functions that the user can specify.

    Args:
        value (typing.Any): Any value.
    Returns:
        (Maybe) A Maybe monad which wraps the exact value given.
    """
    return Maybe(value)


def bind_maybe(maybe: Maybe, function: typing.Callable) -> Maybe:
    """Binds a function to a Maybe monad.

    This function implements rigorous type checking to ensure that the function supplied is of the correct type. It then binds a
    function to a monad and returns a new Maybe instance, unlike the bind class method.

    Args:
        maybe (Maybe): A maybe monad, which may be in any state.
        function (typing.Callable): A function which takes a value of the same type as maybe.value and returns a Maybe monad.
    Returns:
        (Maybe) A maybe monad with the correct state and value as specified by the function given.
    """
    fn_type_signature = inspect.signature(function)
    return_t = fn_type_signature.return_annotation

    if (
        len(fn_type_signature.parameters) != 1 or
        ( return_t is not function_type_signature.empty and return_t != Maybe )
    ):
        raise TypeError(
            "Function passed to bind_maybe violates Monad laws, must take one argument and return a Maybe.\n"
            "The function's type signature is {}".format(str(fn_type_signature))
        )

    maybe_val = copy.deepcopy(maybe.value)
    new_maybe: Maybe = function(record_val)

    if new_maybe.is_nothing():
        new_val = None
    else:
        new_val = new_maybe.value

    return Maybe(
        value = new_val,
        maybe = new_maybe.maybe
    )


def fmap_maybe(maybe: Maybe, function: typing.Callable) -> Maybe:
    """Performs a functor map on a Maybe monad.

    Functor mapping involves taking a function and applying it to the monad's value without modifying the current state.

    Args:
        maybe (Maybe): A Maybe monad, in any state.
        function (typing.Callable): A function to be applied to the monad's value, it must take a single argument of the same type
                                    as maybe.value and return anything.
    Returns:
        (Maybe) A maybe monad whose value has been modified by the supplied function. If the input monad was in the failure state
        the output value will remain unchanged and None.
    """
    fn_type_signature = typing.signature(function)
    return_t: type = fn_type_signature.return_annotation

    if len(fn_type_signature.parameters) != 1:
        raise TypeError("placeholder")

    if maybe.is_just():
        maybe_val: typing.Any = copy.deepcopy(maybe.value)
        new_maybe_val: Maybe = function(maybe_val)
        return Maybe(new_maybe_val)
    elif maybe.is_nothing():
        return Maybe(None, maybe = "nothing")

