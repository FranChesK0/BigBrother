import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class Attend:
    student_id: int
    class_number: int
    attend: bool


@dataclass(frozen=True)
class Student:
    student_id: int
    last_name: str
    first_name: str
    middle_name: str
    group_id: int
    face: dict[str]


@dataclass(frozen=True)
class Schedule:
    class_number: int
    begin_time: datetime.datetime
    end_time: datetime.datetime
