from enum import Enum
from datetime import date

from pydantic import BaseModel
from pydantic.types import PositiveInt, conint, constr


NAME_REGEX = r"^[A-Za-z -'éèï]{2,25}$"


class Gender(Enum):
    Male = 'M'
    Female = 'F'


class Player(BaseModel):
    id: PositiveInt
    last_name: constr(regex=NAME_REGEX, strict=True)
    first_name: constr(regex=NAME_REGEX, strict=True)
    birth_date: date
    gender: Gender
    rank: conint(ge=0, le=3000, strict=True)

    def __str__(self):
        return f"{self.last_name.upper()} {self.first_name} - {self.rank}"

    @property
    def name(self):
        return f"{self.last_name.upper()} {self.first_name.capitalize()}"
