import unittest
from unittest.mock import Mock

import pandas as pd

from src.BigExamsEarly import BigExamsEarly
from src.SpecialProfessors import SpecialProfessors
from src.DataManager import DataManager
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


if __name__ == '__main__':
    unittest.main()
