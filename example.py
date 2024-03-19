#!/usr/bin/python3

import numpy as np

from maybe import Maybe
from do import do


def main():
    """
    Demonstrates the use of a maybe monad and a do function for listing binds.
    """
    q = Quadratic(4,2,1)





class Quadratic:


    def __init__(self, a: int|float, b: int|float, c: int|float) -> None:
        self.a, self.b, self.c = a, b, c


    def __str__(self) -> str:
        a_sign, b_sign, c_sign = "-", "-", "-"
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
        pass




if __name__=="__main__":
    main()
