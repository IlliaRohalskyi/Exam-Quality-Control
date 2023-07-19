from rule_components.RoomCapacity import RoomCapacity
from rule_components.RoomDistance import RoomDistance
from rule_components.BigExamsEarly import BigExamsEarly
from rule_components.OneExamPerDay import OneExamPerDay
from rule_components.SpecialProfessors import SpecialProfessors
from rule_components.OneDayGap import OneDayGap
from rule_components.SpecialDates import SpecialDates
from data_components.DataManager import DataManager
import configparser
import os

config = configparser.ConfigParser()


this_file_path = os.path.abspath(__file__)
this_folder_path = os.path.dirname(this_file_path)
src_folder_path = os.path.dirname(this_folder_path)
project_folder_path = os.path.dirname(src_folder_path)
config.read(os.path.join(project_folder_path, 'config.ini'))
def get_data_file_path(filedir):
    data_file_path = os.path.join(project_folder_path, filedir)
    return data_file_path

exam_plan_path = get_data_file_path(config.get('FilePaths', 'exam_plan_path'))
registration_info_path = get_data_file_path(config.get('FilePaths', 'registration_info_path'))
room_distances_path = get_data_file_path(config.get('FilePaths', 'room_distances_path'))
room_capacities_path = get_data_file_path(config.get('FilePaths', 'room_capacities_path'))
special_dates_path = get_data_file_path(config.get('FilePaths', 'special_dates_path'))
special_examiner_path = get_data_file_path(config.get('FilePaths', 'special_examiner_path'))


class Scoring():

    def __init__(self):
        data_manager = DataManager()
        data_obj = data_manager.get_data_instance(exam_plan_path, registration_info_path, room_distances_path,
                                                  room_capacities_path, special_dates_path, special_examiner_path)

        self.big_exams_early = BigExamsEarly(data_obj)
        self.one_exam_per_day = OneExamPerDay(data_obj)
        self.room_capacity = RoomCapacity(data_obj)
        self.room_distances = RoomDistance(data_obj)
        self.special_professors = SpecialProfessors(data_obj)
        self.one_day_gap = OneDayGap(data_obj)
        self.special_dates = SpecialDates(data_obj)


scoring = Scoring()
