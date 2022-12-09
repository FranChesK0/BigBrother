import datetime
from dataclasses import dataclass
from abc import ABC


@dataclass(frozen=True)
class DBObjectBase(ABC):
    pass

@dataclass(frozen=True)
class Attend(DBObjectBase):
    student_id: int
    class_number: int
    attend_time: datetime.datetime


@dataclass(frozen=True)
class Student(DBObjectBase):
    student_id: int
    group_id: int
    last_name: str
    first_name: str
    middle_name: str
    face: bytes


@dataclass(frozen=True)
class ScheduleRecord(DBObjectBase):
    class_number: int
    begin_time: datetime.datetime
    end_time: datetime.datetime
    group_id: int


@dataclass(frozen=True)
class Group(DBObjectBase):
    group_id: int
    group_name: str
