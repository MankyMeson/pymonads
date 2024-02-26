import typing
import copy
import inspect


class Record:


    def __init__(self, value, log: list[str] = []):
        """
        Initialises a record monad instance.
        """
        self.value = value
        self.log = log


    def __str__(self):
        return (
            "Value:\n"
            "    {}\n"
            "Logs:\n"
            "{}".format(
                self.value,
                "\n".join(["    " + elem for elem in self.log])
            )
        )


    def bind(self, function: typing.Callable):
        new_record = bind_record(self, function)
        self.value, self.log = new_record.value, new_record.log


def return_record(value) -> Record:
    return Record(value)


def bind_record(record: Record, function: typing.Callable) -> Record:
    function_type_signature = inspect.signature(function)
    return_t = function_type_signature.return_annotation

    if (
        len(function_type_signature.parameters) != 1 or
        ( return_t is not function_type_signature.empty and return_t != Record)
    ):
        raise TypeError(
            """
            Function passed to bind_record violates Monad laws, must take one argument and return a Record.
            The function's type signature is {}
            """.format(str(function_type_signature))
        )

    record_val = copy.deepcopy(record.value)
    new_record: Record = function(record_val)

    return Record(
        value = new_record.value,
        log = record.log + new_record.log
    )


def fmap_record(record: Record, function: typing.Callable) -> Record:
    fn_type_signature = typing.signature(function)
    return_t: type = fn_type_signature.return_annotation

    if len(fn_type_signature.parameters) != 1:
        raise TypeError("Function has too many arguments.")

    Return Record(
        value = function(record.value),
        log = record.log
    )


# Example functions.
if __name__=="__main__":

    def square_record(x: int|float) -> Record:
        x2 = x**2
        return Record(
            value = x2,
            log = ["{} was squared to obtain {}".format(x, x2)]
        )

# This function cannot be bound by default, so must have exactly one argument filled before being bound. This would be much easier
# in Haskell but I've already committed
    def multiply_record(x: int|float, y: int|float) -> Record:
        xy = x * y
        return Record(
            value = xy,
            log = ["{} and {} were multiplied to obtain {}".format(x, y, xy)]
        )


    class Person:


        def __init__(self, name, pet = None, favourite_food = None):
            self.name = name
            self.pet = pet
            self.favourite_food = favourite_food


        def __str__(self):
            out_str = self.name + " is a human "
            if self.pet is not None:
                out_str += "who owns a pet called " + self.pet + " "
            if self.favourite_food is not None:
                out_str += "and their favourite food is " + self.favourite_food
            return out_str


    def person_pet_get(person: Person) -> Record:
        if person.pet is not None:
            return Record(
                value = person,
                log = ["Pet named {} is owned by person {}".format(person.pet, person.name)]
            )
        else:
            return Record(
                    value = person,
                    log = ["No pet was found to be owned by person {}".format(person.name)]
            )

    def person_pet_give(person: Person, pet_name: str) -> Record:
        if person.pet is None:
            return Record(
                value = Person(person.name, pet = pet_name, favourite_food = person.favourite_food),
                log = ["Pet named " + pet_name + " was given to " + person.name]
            )


    def test_monad():
        my_record = Record(value = 5)
        print(my_record)
        print()
        my_record.bind(square_record)
        print(my_record)
        print()
        my_record.bind(square_record)
        print(my_record)
        print()
        my_record.bind((lambda x: multiply_record(x, 12)))
        print(my_record)
        print()
        my_record.bind(lambda x: multiply_record(x, 0.01))
        print(my_record)
        print()

        my_person_record = Record(value = Person("Clio"))
        print(my_person_record)
        print()
        my_person_record.bind(person_pet_get)
        print(my_person_record)
        print()
        my_person_record.bind(lambda person: person_pet_give(person, "Vincent"))
        print(my_person_record)
        print()
        my_person_record.bind(person_pet_get)
        print(my_person_record)
        print()

    test_monad()
