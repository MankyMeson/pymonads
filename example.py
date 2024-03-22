#!/usr/bin/python3

import numpy as np
import math

from maybe import Maybe
from do import do

EPSILON = 10e-11


def main():
    """
    Demonstrates the use of a maybe monad and a do function for listing binds.
    """
    q = Quadratic(4,2,1)
    print(
        "Quadratic equation solver:\n"
        "Solving equation " + str(q)
    )
    maybe_result = quadratic_roots(q)
    print("No real roots" if maybe_result.is_nothing() else "{}".format(maybe_result.value))


class Quadratic:


    def __init__(self, a: int|float, b: int|float, c: int|float) -> None:
        self.a, self.b, self.c = a, b, c
        self.discriminant = self.discriminant()


    def __str__(self) -> str:
        b_sign, c_sign = "-", "-", "-"
        if self.b >= 0: b_sign: str = "+"
        if self.c >= 0: c_sign: str = "+"

        format_vars = a, b_sign, b, c_sign, c
        if self.a >= 0:
            return "{}x^2 {} {}x {} {} = 0".format(*format_vars)
        else:
            return "-{}x^2 {} {}x {} {} = 0".format(*format_vars)


    def discriminant(self) -> float:
        return self.b**2 - 4 * self.a * self.c


    def roots(self):
        one_over_2a = -0.5 / self.a
        if self.discriminant < 0:
            return None
        elif self.discriminant == 0 or (self.discriminant < EPSILON and self.discriminant > 0):
            return -0.5 * self.b / self.a
        elif self.discriminant > 0:
            return -0.5 * (self.b + math.sqrt(discriminant)) / self.a, -0.5 * (self.b - math.sqrt(discriminant)) / self.a


def quadratic_roots(eqn: Quadtratic) -> Maybe:
    half_inv_a = 0.5 / self.a
    if eqn.discriminant < 0.:
        return Maybe(
            value = None,
            maybe = "nothing"
        )
    elif eqn.discriminant == 0. or (eqn.discriminant < EPSILON and self.discriminant > 0.):
        return Maybe(
            value = -half_inv_a * eqn.b,
            maybe = "just"
        )
    elif eqn.discriminant > 0.:
        return Maybe(
            value = (
                -half_inv_a * (eqn.b + math.sqrt(discriminant)),
                -half_inv_a * (eqn.b - math.sqrt(discriminant))
            ),
            maybe = "just"
        )



if __name__=="__main__":
    main()
