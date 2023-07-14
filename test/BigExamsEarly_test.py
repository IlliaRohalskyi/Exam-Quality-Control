import unittest

from src.BigExamsEarly import BigExamsEarly
from src.DataManager import DataManager

exam_plan_path = "input_data_files/FIW_Exams_test.xlsx"
registration_info_path = "input_data_files/Pruefungsanmeldungen_anonmous.csv"
room_distances_path = "input_data_files/room_distance_matrix.xlsx"
room_capacities_path = "input_data_files/capacity.json"
special_dates_path = "input_data_files/special_dates.csv"
special_examiner_path = "input_data_files/specific_professors.xlsx"


def test_big_exams_early():
    data_manager = DataManager()
    data = data_manager.get_data_instance(exam_plan_path, registration_info_path, room_distances_path,
                                                  room_capacities_path, special_dates_path, special_examiner_path)

    return BigExamsEarly(data)


asd = test_big_exams_early()
