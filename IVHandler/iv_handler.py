import datetime
import pickle
from abc import ABC, abstractmethod

import cv2
import face_recognition

from RequestHandler.DBTypes import ScheduleRecord, Student, Attend
from RequestHandler.request_handler import RequestHandler


class BaseIVHandler(ABC):
    def __init__(self, database: str):
        self.requests = RequestHandler(database)
        self.face_cascade = cv2.CascadeClassifier('C:\PrgFiles\BigBrother\haarcascade_frontalface_alt2.xml')
        self.video_capture = cv2.VideoCapture(0)

        self.class_number = 0
        self.marked: set[str] = set()
        self.upload_data: list[Attend] = list()

    def __del__(self):
        self.video_capture.release()
        cv2.destroyAllWindows()

    def run(self):
        while True:
            response = self.requests.select_one("Schedule", f"class_number = {self.class_number}")
            if response is not None:
                current_class: ScheduleRecord = ScheduleRecord(*response)
                students: list[Student] = [Student(*request) for request
                                           in self.requests.select_all("Students",
                                                                       f"group_id == {current_class.group_id}")]

                self.marked.clear()
                self.upload_data.clear()
                cur_len_marked = 0
                while True:
                    _, frame = self.video_capture.read()
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    encodings = face_recognition.face_encodings(rgb)

                    for encoding in encodings:
                        matches = face_recognition.compare_faces([pickle.loads(student.face)
                                                                  for student in students], encoding)

                        if any(matches):
                            matched_ids = [i for i, b in enumerate(matches) if b]
                            counts = {}

                            for i in matched_ids:
                                stud_id = students[i].student_id
                                counts[stud_id] = counts.get(stud_id, 0) + 1
                            stud_id = max(counts, key=counts.get)

                        cur_student: Student
                        for stud in students:
                            if stud_id == stud.student_id:
                                cur_student = stud
                                break

                        self.marked.add(f"{cur_student.first_name} {cur_student.last_name} {cur_student.middle_name}")
                        self.upload_data.append(Attend(cur_student.student_id,
                                                       self.class_number,
                                                       datetime.datetime.now()))

                    if self.marked != cur_len_marked:
                        cur_len_marked = len(self.marked)
                        self.__show_students()

                    if current_class.end_time <= datetime.datetime.now():
                        break

            self.requests.insert_many("Attends", self.upload_data)
            self.class_number = (self.class_number + 1) % 7

    def __show_students(self):
        raise NotImplementedError


class ConsoleIVHandler(BaseIVHandler):
    def __show_students(self):
        [print(student) for student in self.marked]
