import re
from typing import Callable


class Pattern(str):
    def __new__(cls, v: str, regex: str):
        """ Subclass of string class, only creates if regex match """
        v = str(v)
        if not re.match(regex, v):
            raise ValueError
        return str.__new__(cls, v)


class Name(Pattern):
    def __new__(cls, v):
        """ Subclass of Pattern, returns a string which matches with the regex """
        return Pattern.__new__(cls, v, regex=r"^[A-Za-z -'éèï]{2,25}$")


class ConInt(int):
    """ Subclass of Integer, valid only if check is True """
    def __new__(cls, v: int, check: Callable):
        v = int(v)
        if not check(v):
            raise ValueError
        return int.__new__(cls, v)


class Rank(ConInt):
    """ Subclass of ConInt, only valid with int between 1 and 3000"""
    def __new__(cls, v):
        return ConInt.__new__(cls, v, check=lambda x: x in range(1, 3001))
