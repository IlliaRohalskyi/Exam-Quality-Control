import unittest
from unittest.mock import Mock

import pandas as pd

from src.BigExamsEarly import BigExamsEarly
from src.SpecialProfessors import SpecialProfessors
from src.DataManager import DataManager
from src.RoomCapacity import RoomCapacity
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')

exam_plan_path = config.get('FilePaths', 'exam_plan_path')
registration_info_path = config.get('FilePaths', 'registration_info_path')
room_distances_path = config.get('FilePaths', 'room_distances_path')
room_capacities_path = config.get('FilePaths', 'room_capacities_path')
special_dates_path = config.get('FilePaths', 'special_dates_path')
special_examiner_path = config.get('FilePaths', 'special_examiner_path')


class Test(unittest.TestCase):

    def test_big_exams_early(self):
        data_manager = DataManager()
        data = data_manager.get_data_instance(exam_plan_path,
                                              registration_info_path,
                                              room_distances_path,
                                              room_capacities_path,
                                              special_dates_path,
                                              special_examiner_path)

        big_exams_early = BigExamsEarly(data)

        self.assertGreaterEqual(big_exams_early.score, 70)

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
