import datetime

from DataHandler.data_handler import DataHandler
from RequestHandler.DBTypes import ScheduleRecord


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

        self.actions: dict[str] = {
            "1": lambda: self.__schedule_menu.run(),
        }

    def run(self) -> None:
        while (True):
            print("\033[H\033[2J", end="")

            print("Выберите, с какой частью бд взаимодействовать:")
            print("[1] Расписание")
            print("[2] Студенты")
            print("[3] Группы")
            print("[4] Посещения")
            print("[5] Выход из программы")

            choice: str = input("Ваш выбор: ")            
            print("\033[H\033[2J", end="")

            if (choice == "5"):
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

            print("[S] Показать расписание")
            print("[C] Очистить расписание")
            print("[A] Добавить пару")
            print("[E] Редактировать пару")
            print("[R] Удалить пару")
            print("[B] Вернуться назад")

            choice: str = input("Ваш выбор: ")

            print("\033[H\033[2J", end="")
            if (choice == "S"):
                schedule: list[ScheduleRecord] = self.__dh.get_schedule()
                if (len(schedule) == 0):
                    print("Расписание пусто")
                else:
                    for r in self.__dh.get_schedule():
                        print("[{}] Группа {}; С {} до {}".format(
                            r.class_number, r.group_id, r.begin_time, r.end_time
                        ))

            elif (choice == "C"):
                self.__dh.clear_schedule()
                print("Расписание очищено")

            elif (choice == "A"):
                cn: int = int(input("Введите номер пары: "))
                gi: int = int(input("Введите номер группы: "))

                self.__dh.add_schedule_record(ScheduleRecord(
                    cn, self.get_dt(date, timestamps[cn]),
                    self.get_dt(date, timestamps[cn+1]), gi
                ))

            elif (choice == "B"):
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
