from RequestHandler.request_handler import RequestHandler
from RequestHandler.DBTypes import Student, ScheduleRecord, Group


class DataHandler:
    def __init__(self, db_path: str) -> None:
        self.__rh: RequestHandler = RequestHandler(db_path)

    def get_student(self, student_id: int) -> Student | None:
        r = self.__rh.select_one(
            "Schedule", f"student_id = {student_id}"
        )

        return Student(*r) if r else None

    def add_student(self, student: Student):
        self.__rh.insert_one(
            "Students", student,
            "group_id", "last_name", "first_name", "middle_name", "face"
        )

    def add_students(self, students: list[Student]):
        self.__rh.insert_many(
            "Students", students,
            "group_id", "last_name", "first_name", "middle_name", "face"
        )

    def delete_student(self, student_id: int):
        self.__rh.delete_all("Students", f"student_id = {student_id}")

    def add_group(self, group: Group):
        self.__rh.insert_one("Groups", group, "group_name")

    def delete_group(self, group_id: int):
        self.__rh.delete_all("Group", f"group_id = {group_id}")

    def add_schedule_record(self, record: ScheduleRecord):
        self.__rh.insert_one("Schedule", record)

    def get_schedule(self) -> list[ScheduleRecord]:
        return [ScheduleRecord(*r) for r in self.__rh.select_all("Schedule")]

    def get_schedule_record(self, class_number: int) -> ScheduleRecord | None:
        r = self.__rh.select_one(
            "Schedule", f"class_number = {class_number}"
        )

        return ScheduleRecord(*r) if r else None

    def add_schedule(self, schedule: list[ScheduleRecord]):
        self.__rh.insert_many("Schedule", schedule)

    def clear_schedule(self):
        self.__rh.delete_all("Schedule")
