from RoomCapacity import RoomCapacity
from RoomDistance import RoomDistance
from BigExamsEarly import BigExamsEarly
from OneExamPerDay import OneExamPerDay
from SpecialProfessors import SpecialProfessors
from OneDayGap import OneDayGap
from SpecialDates import SpecialDates
from src.DataManager import DataManager
import configparser

config = configparser.ConfigParser()
config.read('/Users/mbr/PycharmProjects/project/config.ini')

exam_plan_path = config.get('FilePaths', 'exam_plan_path')
registration_info_path = config.get('FilePaths', 'registration_info_path')
room_distances_path = config.get('FilePaths', 'room_distances_path')
room_capacities_path = config.get('FilePaths', 'room_capacities_path')
special_dates_path = config.get('FilePaths', 'special_dates_path')
special_examiner_path = config.get('FilePaths', 'special_examiner_path')


class Scoring():

    def __init__(self):
        data_manager = DataManager()
        data = data_manager.get_data_instance(exam_plan_path, registration_info_path, room_distances_path,
                                              room_capacities_path, special_dates_path, special_examiner_path)

        self.big_exams_early = BigExamsEarly(data)
        self.one_exam_per_day = OneExamPerDay()
        self.room_capacity = RoomCapacity()
        self.room_distances = RoomDistance()
        self.special_professors = SpecialProfessors()
        self.one_day_gap = OneDayGap()
        self.special_dates = SpecialDates()


scoring = Scoring()
