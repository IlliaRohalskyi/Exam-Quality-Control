import unittest
from unittest.mock import Mock

import pandas as pd
import numpy as np
from datetime import datetime

from src.data_components.DataManager import DataManager
from src.rule_components.BigExamsEarly import BigExamsEarly
from src.rule_components.OneExamPerDay import OneExamPerDay
from src.rule_components.SpecialProfessors import SpecialProfessors
from src.rule_components.RoomCapacity import RoomCapacity
from src.rule_components.RoomDistance import RoomDistance
from src.rule_components.OneDayGap import OneDayGap
from src.rule_components.SpecialDates import SpecialDates

import configparser

exam_plan_path = 'input_data_files/FIW_Exams_2022ws.xlsx'
registration_info_path = 'input_data_files/Pruefungsanmeldungen_anonmous.csv'
room_distances_path = 'input_data_files/room_distance_matrix.xlsx'
room_capacities_path = 'input_data_files/capacity.json'
special_dates_path = 'input_data_files/special_dates.csv'
special_examiner_path = 'input_data_files/specific_professors.xlsx'

data_manager = DataManager()
data_obj = data_manager.get_data_instance(exam_plan_path,
                                          registration_info_path,
                                          room_distances_path,
                                          room_capacities_path,
                                          special_dates_path,
                                          special_examiner_path)
class Test(unittest.TestCase):

    def test_big_exams_early_best(self):
        def get_mock_data():
            mock_data = Mock()

            mock_data.number_of_students = np.array([300, 225, 200, 150, 125, 70, 60, 45, 30, 5])
            mock_data.start_date = pd.Series([
                datetime(2023, 7, 1),
                datetime(2023, 7, 3),
                datetime(2023, 7, 5),
                datetime(2023, 7, 7),
                datetime(2023, 7, 9),
                datetime(2023, 7, 11),
                datetime(2023, 7, 13),
                datetime(2023, 7, 15),
                datetime(2023, 7, 17),
                datetime(2023, 7, 19)
            ])
            return mock_data

        mock_data = get_mock_data()
        big_exams_early = BigExamsEarly(mock_data)

        print(big_exams_early.score)
        self.assertAlmostEqual(big_exams_early.score, 100)

    def test_big_exams_early_worst(self):
        def get_mock_data():
            mock_data = Mock()
            mock_data.number_of_students = np.array([5, 15, 30, 50, 70, 80, 90, 125, 150, 200])
            mock_data.start_date = pd.Series([
                datetime(2023, 7, 1),
                datetime(2023, 7, 3),
                datetime(2023, 7, 5),
                datetime(2023, 7, 7),
                datetime(2023, 7, 9),
                datetime(2023, 7, 11),
                datetime(2023, 7, 13),
                datetime(2023, 7, 15),
                datetime(2023, 7, 17),
                datetime(2023, 7, 19)
            ])
            return mock_data

        mock_data = get_mock_data()
        big_exams_early = BigExamsEarly(mock_data)

        print(big_exams_early.score)
        self.assertAlmostEqual(big_exams_early.score, 0)

    def test_room_distances_best(self):
        def get_mock_data():
            mock_data = Mock()
            mock_data.exam_rooms = pd.DataFrame({'HS': [['H.1.2', 'H.1.3'],
                                                        ['H.1.2', 'H.1.3'],
                                                        ['H.1.2', 'H.1.3'],
                                                        ['H.1.2', 'H.1.3'],
                                                        ['H.1.2', 'H.1.3'],
                                                        ['H.1.2', 'H.1.3']]})

            mock_data.exam_form = pd.DataFrame({'Form': ['schriftlich',
                                                         'schriftlich',
                                                         'schriftlich',
                                                         'schriftlich',
                                                         'schriftlich',
                                                         'schriftlich']})

            mock_data.room_distances = data_obj.room_distances
            return mock_data

        room_distances = RoomDistance(get_mock_data())
        print(room_distances.score)
        self.assertAlmostEqual(room_distances.score, 100)

    def test_room_distances_worst(self):
        def get_mock_data():
            mock_data = Mock()
            mock_data.exam_rooms = pd.DataFrame({'HS': [['H.1.11', 'I.3.19'],
                                                        ['H.1.11', 'I.3.19'],
                                                        ['H.1.11', 'I.3.19'],
                                                        ['H.1.11', 'I.3.19'],
                                                        ['H.1.11', 'I.3.19'],
                                                        ['H.1.11', 'I.3.19']]})

            mock_data.exam_form = pd.DataFrame({'Form': ['schriftlich',
                                                         'schriftlich',
                                                         'schriftlich',
                                                         'schriftlich',
                                                         'schriftlich',
                                                         'schriftlich']})

            mock_data.room_distances = data_obj.room_distances
            return mock_data

        room_distances = RoomDistance(get_mock_data())
        print(room_distances.score)
        self.assertAlmostEqual(room_distances.score, 0)

    def test_special_professors_best(self):
        def get_mock_data():
            mock_data = Mock()
            mock_data.examiner = pd.DataFrame({'1. & 2. Pruefer': [['prof1', 'prof2'], ['prof3', 'prof4'],
                                                                   ['prof1', 'prof6'], ['prof7', 'prof6'],
                                                                   ['prof9', 'prof10'],['prof3', 'prof4'],
                                                                   ['prof3', 'prof4']]})
            mock_data.start_date = pd.DataFrame(
                {'start_date': [pd.Timestamp('2023-07-15'),
                                pd.Timestamp('2023-07-16'),
                                pd.Timestamp('2023-07-15'),
                                pd.Timestamp('2023-07-16'),
                                pd.Timestamp('2023-07-17'),
                                pd.Timestamp('2023-07-16'),
                                pd.Timestamp('2023-07-16')
                                ]})
            mock_data.course_name = pd.DataFrame({'Lehrveranstaltung': ['Course1',
                                                                        'Course2',
                                                                        'Course3',
                                                                        'Course4'
                                                                        'Course5',
                                                                        'Course6',
                                                                        'Course7'
                                                                        ]})
            mock_data.special_examiners = pd.DataFrame({'Professor': ['prof1',
                                                                      'prof3',
                                                                      'prof4']})
            return mock_data

        mock_data = get_mock_data()
        special_professors = SpecialProfessors(mock_data)
        print(special_professors.score)
        self.assertAlmostEqual(special_professors.score, 100)

    def test_special_professors_worst(self):
        def get_mock_data():
            mock_data = Mock()
            mock_data.examiner = pd.DataFrame({'1. & 2. Pruefer': [['prof1', 'prof2'], ['prof3', 'prof4'],
                                                                   ['prof1', 'prof6'], ['prof3', 'prof6'],
                                                                   ['prof3', 'prof10']]})
            mock_data.start_date = pd.DataFrame(
                {'start_date': [pd.Timestamp('2023-07-15'),
                                pd.Timestamp('2023-07-16'),
                                pd.Timestamp('2023-07-17'),
                                pd.Timestamp('2023-07-18'),
                                pd.Timestamp('2023-07-19')
                                ]})
            mock_data.course_name = pd.DataFrame({'Lehrveranstaltung': ['Course1',
                                                                        'Course2',
                                                                        'Course3',
                                                                        'Course4',
                                                                        'Course5']})
            mock_data.special_examiners = pd.DataFrame({'Professor': ['prof1',
                                                                      'prof3',
                                                                      ]})
            return mock_data

        mock_data = get_mock_data()
        special_professors = SpecialProfessors(mock_data)
        print(special_professors.score)
        self.assertAlmostEqual(special_professors.score, 0)

    def test_special_dates_best(self):
        def get_mock_data():
            mock_data = Mock()
            mock_data.special_dates_df = pd.DataFrame({'lastName': ['Examiner1',
                                                                    'Examiner2',
                                                                    'Examiner3'],
                                                       'specialDate': ['2023-01-27',
                                                                       '2023-01-27',
                                                                       '2023-01-27']})

            mock_data.examiners_exams_df = pd.DataFrame({'1. & 2. Pruefer': [['Examiner1', 'Examiner2'],
                                                                             ['Examiner3', 'Examiner4'],
                                                                             ['Examiner5', 'Examiner6'],
                                                                             ['Examiner7', 'Examiner8'],
                                                                             ['Examiner9', 'Examiner10']],

                                                         'Datum, Uhrzeit (ggf. sep. Zeitplan beachten)': [
                                                             '2023-01-25T11:00 - 2023-01-25T12:30',
                                                             '2023-01-26T11:00 - 2023-01-26T12:30',
                                                             '2023-01-27T11:00 - 2023-01-27T12:30',
                                                             '2023-01-28T11:00 - 2023-01-28T12:30',
                                                             '2023-01-29T11:00 - 2023-01-29T12:30']})
            return mock_data

        special_dates = SpecialDates(get_mock_data())
        print(special_dates.score)
        print(special_dates.conflicts_df)
        self.assertAlmostEqual(special_dates.score, 100)

    def test_special_dates_worst(self):
        def get_mock_data():
            mock_data = Mock()
            mock_data.special_dates_df = pd.DataFrame({'lastName': ['Examiner1',
                                                                    'Examiner2',
                                                                    'Examiner3'],
                                                       'specialDate': ['2023-01-25',
                                                                       '2023-01-25',
                                                                       '2023-01-26']})

            mock_data.examiners_exams_df = pd.DataFrame({'1. & 2. Pruefer': [['Examiner1', 'Examiner2'],
                                                                             ['Examiner3', 'Examiner4'],
                                                                             ['Examiner5', 'Examiner6'],
                                                                             ['Examiner7', 'Examiner8'],
                                                                             ['Examiner9', 'Examiner10']],

                                                         'Datum, Uhrzeit (ggf. sep. Zeitplan beachten)': [
                                                             '2023-01-25T11:00 - 2023-01-25T12:30',
                                                             '2023-01-26T11:00 - 2023-01-26T12:30',
                                                             '2023-01-27T11:00 - 2023-01-27T12:30',
                                                             '2023-01-28T11:00 - 2023-01-28T12:30',
                                                             '2023-01-29T11:00 - 2023-01-29T12:30']})
            return mock_data

        special_dates = SpecialDates(get_mock_data())
        print(special_dates.score)
        print(special_dates.conflicts_df)
        self.assertAlmostEqual(special_dates.score, 0)

    def test_one_day_gap(self):
        def get_mock_data():
            mock_data = Mock()

            mock_data.course_stud = pd.DataFrame({
                'coursenr': ['course1', 'course2', 'course3', 'course4'],
                'matnr': [['stud1', 'stud2'], ['stud3', 'stud4', 'stud5'], ['stud2', 'stud3'], ['stud1', 'stud4']]
            })

            mock_data.splitted_df = pd.DataFrame({
                'LV-Nr.': ['course1', 'course2', 'course3', 'course4'],
                'start_date': [
                    pd.Timestamp('2023-07-15'),
                    pd.Timestamp('2023-07-17'),
                    pd.Timestamp('2023-07-19'),
                    pd.Timestamp('2023-07-21')
                ],
                'Lehrveranstaltung': ['Course1', 'Course2', 'Course3', 'Course4']
            })

            mock_data.reg_info = pd.DataFrame({'matnr': ['stud1', 'stud2', 'stud3', 'stud4', 'stud5']})

            return mock_data

        mock_data = get_mock_data()
        one_day_gap = OneDayGap(mock_data)

        print(one_day_gap.score)
        self.assertAlmostEqual(one_day_gap.score, 100)

    def test_one_exam_per_day_best(self):
        def get_mock_data():
            mock_data = Mock()

            mock_data.course_stud = pd.DataFrame({
                'coursenr': ['coursenr1', 'coursenr2', 'coursenr3', 'coursenr4', 'coursenr5'],
                'matnr': [['student1', 'student2'],
                          ['student1', 'student2'],
                          ['student1', 'student2'],
                          ['student1', 'student2'],
                          ['student1', 'student2']]
            })

            mock_data.splitted_df = pd.DataFrame({
                'LV-Nr.': ['coursenr1', 'coursenr2', 'coursenr3', 'coursenr4', 'coursenr5'],
                'Lehrveranstaltung': ['Exam1', 'Exam2', 'Exam3', 'Exam4', 'Exam5'],
                'start_date': ['2023-07-01', '2023-07-02', '2023-07-03', '2023-07-04', '2023-07-05']
            })

            mock_data.reg_info = pd.DataFrame({'matnr': ['stud1', 'stud2']})

            return mock_data

        mock_data = get_mock_data()
        one_exam_per_day = OneExamPerDay(mock_data)
        print(one_exam_per_day.score)
        print(one_exam_per_day.conflicts_df)

        self.assertAlmostEqual(one_exam_per_day.score, 100)

    def test_one_exam_per_day_worst(self):
        def get_mock_data():
            mock_data = Mock()

            mock_data.course_stud = pd.DataFrame({
                'coursenr': ['coursenr1', 'coursenr2', 'coursenr3', 'coursenr4', 'coursenr5'],
                'matnr': [['student1', 'student2'],
                          ['student1', 'student2'],
                          ['student1', 'student2'],
                          ['student1', 'student2'],
                          ['student1', 'student2']]
            })

            mock_data.splitted_df = pd.DataFrame({
                'LV-Nr.': ['coursenr1', 'coursenr2', 'coursenr3', 'coursenr4', 'coursenr5'],
                'Lehrveranstaltung': ['Exam1', 'Exam2', 'Exam3', 'Exam4', 'Exam5'],
                'start_date': ['2023-07-01', '2023-07-01', '2023-07-01', '2023-07-01', '2023-07-01']
            })

            mock_data.reg_info = pd.DataFrame({'matnr': ['stud1', 'stud2']})

            return mock_data

        mock_data = get_mock_data()
        one_exam_per_day = OneExamPerDay(mock_data)
        print(one_exam_per_day.score)
        print(one_exam_per_day.conflicts_df)

        self.assertAlmostEqual(one_exam_per_day.score, 0)

    def test_room_capacity_best(self):
        def get_mock_data():
            mock_data = Mock()
            mock_data.course_stud = pd.DataFrame({
                'coursenr': ['course1', 'course2', 'course3', 'course4'],
                'matnr': [
                    ['stud1', 'stud2', 'stud3', 'stud4', 'stud5', 'stud6'],
                    ['stud7', 'stud8', 'stud9', 'stud10'],
                    ['stud11', 'stud12', 'stud13', 'stud14', 'stud15'],
                    ['stud16', 'stud17']
                ]
            })

            mock_data.exam_plan = pd.DataFrame({
                'LV-Nr.': ['course1', 'course2', 'course3', 'course4'],
                'HS': [['H.1.1'], ['H.1.2'], ['H.1.3'], ['H.1.1']]
            })

            mock_data.room_capacities = {
                'Exam-room-capacities': {
                    'Horsaal': [
                        {'Name': 'H.1.1', 'Klausur-capacity 1': 6, 'Klausur-capacity 2': 6},
                        {'Name': 'H.1.2', 'Klausur-capacity 1': 4, 'Klausur-capacity 2': 4},
                        {'Name': 'H.1.3', 'Klausur-capacity 1': 5, 'Klausur-capacity 2': 5}
                    ],
                    'Seminar-raum': [{'Name': 'I.2.15', 'Klausur-capacity 1': 15, 'Klausur-capacity 2': 30}],
                    'Raum': [{'Name': 'I.2.1', 'Klausur-capacity 1': 2, 'Klausur-capacity 2': 2}]
                }
            }

            return mock_data

        mock_data = get_mock_data()
        room_capacity = RoomCapacity(mock_data)
        print(room_capacity.score)
        self.assertGreaterEqual(room_capacity.score, 80)

    def test_room_capacity_worst(self):
        def get_mock_data():
            mock_data = Mock()
            mock_data.course_stud = pd.DataFrame({
                'coursenr': ['course1', 'course2', 'course3', 'course4', 'course5', 'course6'],
                'matnr': [
                    ['stud1', 'stud2', 'stud3'],
                    ['stud4', 'stud5', 'stud6', 'stud7'],
                    ['stud8', 'stud9', 'stud10', 'stud11', 'stud12', 'stud13', 'stud14', 'stud15', 'stud16', 'stud17',
                     'stud18', 'stud19', 'stud20'],
                    ['stud21', 'stud22', 'stud23'],
                    ['stud24', 'stud25'],
                    ['stud26', 'stud27', 'stud28', 'stud29', 'stud30', 'stud31', 'stud32', 'stud33', 'stud34', 'stud35',
                     'stud36']
                ]
            })

            mock_data.exam_plan = pd.DataFrame({
                'LV-Nr.': ['course1', 'course2', 'course3', 'course4', 'course5', 'course6'],
                'HS': [['H.1.1'], ['H.1.2'], ['H.1.1', 'H.1.3'], ['H.1.2'], ['H.1.3'], ['I.2.1']]
            })

            mock_data.room_capacities = {
                'Exam-room-capacities': {
                    'Horsaal': [
                        {'Name': 'H.1.1', 'Klausur-capacity 1': 50, 'Klausur-capacity 2': 100},
                        {'Name': 'H.1.2', 'Klausur-capacity 1': 20, 'Klausur-capacity 2': 40},
                        {'Name': 'H.1.3', 'Klausur-capacity 1': 30, 'Klausur-capacity 2': 60}
                    ],
                    'Seminar-raum': [{'Name': 'I.2.15', 'Klausur-capacity 1': 15, 'Klausur-capacity 2': 30}],
                    'Raum': [{'Name': 'I.2.1', 'Klausur-capacity 1': 10, 'Klausur-capacity 2': 20}]
                }
            }

            return mock_data

        mock_data = get_mock_data()
        room_capacity = RoomCapacity(mock_data)
        print(room_capacity.score)
        self.assertLessEqual(room_capacity.score, 10)


if __name__ == '__main__':
    unittest.main()
