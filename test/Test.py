import unittest
from unittest.mock import Mock

import pandas as pd

from src.BigExamsEarly import BigExamsEarly
from src.SpecialProfessors import SpecialProfessors
from src.DataManager import DataManager
from src.RoomCapacity import RoomCapacity
from src.RoomDistance import RoomDistance
from src.OneDayGap import OneDayGap
import configparser

exam_plan_path = 'input_data_files/FIW_Exams_2022ws.xlsx'
registration_info_path = 'input_data_files/Pruefungsanmeldungen_anonmous.csv'
room_distances_path = 'input_data_files/room_distance_matrix.xlsx'
room_capacities_path = 'input_data_files/capacity.json'
special_dates_path = 'input_data_files/special_dates.csv'
special_examiner_path = 'input_data_files/specific_professors.xlsx'
# Testing Files
big_exams_early_best_path = 'input_data_files/big_exams_early_best.xlsx'
big_exams_early_worst_path = 'input_data_files/big_exams_early_worst.xlsx'
room_distances_best_path = 'input_data_files/room_distances_best.xlsx'
room_distances_worst_path = 'input_data_files/room_distances_worst.xlsx'
one_day_gap_worst_path = 'input_data_files/one_day_gap_worst.xlsx'
one_day_gap_best_path = 'input_data_files/one_day_gap_best.xlsx'
registration_info_test_path = 'input_data_files/registirations_test.csv'


class Test(unittest.TestCase):

    def test_big_exams_early_best(self):
        data_manager = DataManager()
        data = data_manager.get_data_instance(big_exams_early_best_path,
                                              registration_info_path,
                                              room_distances_path,
                                              room_capacities_path,
                                              special_dates_path,
                                              special_examiner_path)

        big_exams_early = BigExamsEarly(data)
        print(f'Score: {big_exams_early.score}')
        self.assertGreaterEqual(big_exams_early.score, 70)

    def test_big_exams_early_worst(self):
        data_manager = DataManager()
        data = data_manager.get_data_instance(big_exams_early_worst_path,
                                              registration_info_path,
                                              room_distances_path,
                                              room_capacities_path,
                                              special_dates_path,
                                              special_examiner_path)

        big_exams_early = BigExamsEarly(data)
        print(f'Score: {big_exams_early.score}')
        self.assertLessEqual(big_exams_early.score, 5)

    def test_room_distances_best(self):
        data_manager = DataManager()
        data = data_manager.get_data_instance(room_distances_best_path,
                                              registration_info_test_path,
                                              room_distances_path,
                                              room_capacities_path,
                                              special_dates_path,
                                              special_examiner_path)

        room_distance = RoomDistance(data)
        print(f'Score: {room_distance.score}')
        self.assertAlmostEqual(room_distance.score, 100)

    def test_room_distances_worst(self):
        data_manager = DataManager()
        data = data_manager.get_data_instance(room_distances_worst_path,
                                              registration_info_path,
                                              room_distances_path,
                                              room_capacities_path,
                                              special_dates_path,
                                              special_examiner_path)

        room_distance = RoomDistance(data)
        print(f'Score: {room_distance.score}')
        self.assertAlmostEqual(room_distance.score, 0)

    def test_one_day_gap_best(self):
        data_manager = DataManager()
        data = data_manager.get_data_instance(one_day_gap_best_path,
                                              registration_info_test_path,
                                              room_distances_path,
                                              room_capacities_path,
                                              special_dates_path,
                                              special_examiner_path)

        one_day_gap = OneDayGap(data)
        print(f'Score: {one_day_gap.score}')
        self.assertAlmostEqual(one_day_gap.score, 0)
    def test_one_day_gap_worst(self):
        data_manager = DataManager()
        data = data_manager.get_data_instance(one_day_gap_worst_path,
                                              registration_info_test_path,
                                              room_distances_path,
                                              room_capacities_path,
                                              special_dates_path,
                                              special_examiner_path)

        one_day_gap = OneDayGap(data)
        print(f'Score: {one_day_gap.conflicts_df}')
        self.assertAlmostEqual(one_day_gap.score, 0)
    def test_special_professors(self):
        def get_mock_data():
            mock_data = Mock()
            mock_data.examiner = pd.DataFrame({'1. & 2. Pruefer': [['prof1', 'prof2'], ['prof3', 'prof4'],
                                                                   ['prof3', 'prof1'], ['prof5', 'prof1'],
                                                                   ['prof2', 'prof4']]})
            mock_data.start_date = pd.DataFrame(
                {'start_date': [pd.Timestamp('2023-07-15'),
                                pd.Timestamp('2023-07-16'),
                                pd.Timestamp('2023-07-15'),
                                pd.Timestamp('2023-07-15'),
                                pd.Timestamp('2023-07-19')
                                ]})
            mock_data.course_name = pd.DataFrame({'Lehrveranstaltung': ['Course1',
                                                                        'Course2',
                                                                        'Course3',
                                                                        'Course4'
                                                                        'Course5']})
            mock_data.special_examiners = pd.DataFrame({'Professor': ['prof1',
                                                                      'prof3',
                                                                      ]})
            return mock_data

        mock_data = get_mock_data()
        special_professors = SpecialProfessors(mock_data)
        print(special_professors.score)
        self.assertAlmostEqual(special_professors.score, 50)

    def test_special_dates(self):
        pass

    def test_one_day_gap(self):
        pass

    def test_one_exam_per_day(self):
        pass

    def test_room_capacity(self):
        def get_mock_data():
            mock_data = Mock()
            mock_data.course_stud = pd.DataFrame({
                'coursenr': ['course1', 'course2', 'course3', 'course4'],
                'matnr': [
                    ['stud1', 'stud2'],
                    ['stud3', 'stud4', 'stud5', 'stud6', 'stud7', 'stud8', 'stud9', 'stud10', 'stud11'],
                    ['stud12', 'stud13', 'stud14', 'stud15'],
                    ['stud16']
                ]
            })

            mock_data.exam_plan = pd.DataFrame({
                'LV-Nr.': ['course1', 'course2', 'course3', 'course4'],
                'HS': [['H.1.1'], ['H.1.1', 'H.1.2'], ['H.1.2'], ['room1']]
            })

            mock_data.room_capacities = {
                'Exam-room-capacities': {
                    'Horsaal': [{'Name': 'H.1.1', 'Klausur-capacity 1': 5, 'Klausur-capacity 2': 6},
                                {'Name': 'H.1.2', 'Klausur-capacity 1': 10, 'Klausur-capacity 2': 25}],
                    'Seminar-raum': [{'Name': 'I.2.15', 'Klausur-capacity 1': 15, 'Klausur-capacity 2': 30}],
                    'Raum': [{'Name': 'I.2.1', 'Klausur-capacity 1': 10, 'Klausur-capacity 2': 20}]
                }
            }

            return mock_data

        mock_data = get_mock_data()
        room_capacity = RoomCapacity(mock_data)
        print(room_capacity.score)
        self.assertAlmostEqual(room_capacity.score, 5)



if __name__ == '__main__':
    unittest.main()
