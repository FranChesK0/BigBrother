import datetime

from DataHandler.data_handler import DataHandler
from RequestHandler.DBTypes import Student, ScheduleRecord
from EncodingHandler.encoding_handler import FaceEncoding


date: datetime.date = datetime.date(2022, 12, 12)
timestamps: list[datetime.time] = [
    datetime.time(8, 0), datetime.time(9, 45),
    datetime.time(11, 30), datetime.time(13, 15),
    datetime.time(15, 15), datetime.time(17, 0)
]

class MainMenu:
    def __init__(self, db_path: str) -> None:
        self.__dh: DataHandler = DataHandler(db_path)

        self.__schedule_menu: ScheduleMenu = ScheduleMenu(self.__dh)
        self.__students_menu: StudentsMenu = StudentsMenu(self.__dh)
        self.__groups_menu: GroupsMenu = GroupsMenu(self.__dh)

        self.actions: dict[str] = {
            "1": lambda: self.__schedule_menu.run(),
            "2": lambda: self.__students_menu.run(),
            "3": lambda: self.__groups_menu.run()
        }

    def run(self) -> None:
        while (True):
            print("\033[H\033[2J", end="")

            print("Выберите, с какой частью бд взаимодействовать:")
            print("[1] Расписание")
            print("[2] Студенты")
            print("[3] Группы")
            print("[4] Посещения")
            print("[0] Выход из программы")

            choice: str = input("Ваш выбор: ")            
            print("\033[H\033[2J", end="")

            if (choice == "0"):
                break

            action = self.actions.get(choice)
            if (action is None):
                continue

            action()

class ScheduleMenu:
    def __init__(self, dh: DataHandler) -> None:
        self.__dh: DataHandler = dh

    def run(self) -> None:
        while (True):
            print("\033[H\033[2J", end="")

            print("[1] Показать расписание")
            print("[2] Очистить расписание")
            print("[3] Добавить пару")
            print("[0] Вернуться назад")

            choice: str = input("Ваш выбор: ")

            print("\033[H\033[2J", end="")
            if (choice == "1"):
                schedule: list[ScheduleRecord] = self.__dh.get_schedule()
                if (len(schedule) == 0):
                    print("Расписание пусто")
                else:
                    for r in schedule:
                        print("[{}] Группа {}; С {} до {}".format(
                            r.class_number, r.group_id, r.begin_time, r.end_time
                        ))

            elif (choice == "2"):
                self.__dh.clear_schedule()
                print("Расписание очищено")

            elif (choice == "3"):
                cn: int = int(input("Введите номер пары: "))
                gi: int = int(input("Введите номер группы: "))

                self.__dh.add_schedule_record(ScheduleRecord(
                    cn, self.get_dt(date, timestamps[cn]),
                    self.get_dt(date, timestamps[cn+1]), gi
                ))

            elif (choice == "0"):
                break

            else:
                continue

            input("\nНажмите Enter, Чтобы продолжить")

    @staticmethod
    def get_dt(date: datetime.date, time: datetime.time):
        return datetime.datetime(
            date.year, date.month, date.day,
            time.hour, time.minute
        )


class StudentsMenu:
    def __init__(self, dh: DataHandler) -> None:
        self.__dh: DataHandler = dh

    def run(self) -> None:
        while (True):
            print("\033[H\033[2J", end="")

            print("[1] Добавить студента")
            print("[2] Удалить студента")
            print("[0] Вернуться назад")

            choice: str = input("\nВаш выбор: ")

            print("\033[H\033[2J", end="")
            if (choice == "1"):
                gi: int = int(input("Введите номер группы: "))
                ln, fn, mn = input("Введите ФИО студента: ").split()
                img_path: str = input("Введите путь до фото студента: ")

                self.__dh.add_student(Student(
                    0, gi, ln, fn, mn,
                    FaceEncoding.get_face_encoding(img_path)
                ))

            elif (choice == "2"):
                student_id: int = int(input("Введите id студента: "))
                self.__dh.delete_student(student_id)

                print(f"Студент с id: {student_id} удален")

            elif (choice == "0"):
                break

            else:
                continue

            input("\nНажмите Enter, Чтобы продолжить")


class GroupsMenu:
    def __init__(self, dh: DataHandler) -> None:
        self.__dh: DataHandler = dh

    def run(self) -> None:
        while (True):
            print("\033[H\033[2J", end="")

            print("[1] Показать студентов группы")
            print("[0] Вернуться назад")

            choice: str = input("\nВаш выбор: ")

            print("\033[H\033[2J", end="")
            if (choice == "1"):
                gi: int = int(input("Введите номер группы: "))

                students: list[Student] = self.__dh.get_students(gi)
                if (len(students) == 0):
                    print("В группе никого нет")
                else:
                    print(f"Группа №{gi}:")
                    for r in students:
                        print("[id {}] Студент {} {} {}".format(
                            r.student_id, r.last_name,
                            r.first_name, r.middle_name
                        ))

            elif (choice == "0"):
                break

            else:
                continue

            input("\nНажмите Enter, Чтобы продолжить")
