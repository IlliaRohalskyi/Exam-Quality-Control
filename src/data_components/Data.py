import pandas as pd
import json


class Data:
    def __init__(self, __exam_plan_path, __registration_info_path, __room_distances_path,
                 __room_capacities_path, __special_dates_path, __special_examiners_path):
        # Exam Paths
        self.exam_plan_path = __exam_plan_path
        self.registration_info_path = __registration_info_path
        self.room_distances_path = __room_distances_path
        self.room_capacities_path = __room_capacities_path
        self.special_dates_path = __special_dates_path
        self.special_examiners_path = __special_examiners_path

        # Process exam plan files
        self.exam_plan = self.load_exam_plan(self.exam_plan_path)
        self.room_distances = self.load_room_distances(self.room_distances_path)
        self.room_capacities = self.load_room_capacities(self.room_capacities_path)
        self.special_dates_df = self.load_special_dates(self.special_dates_path)
        self.special_examiners = self.load_special_examiners(self.special_examiners_path)
        self.course_nr, self.mat_nr, self.course_stud, self.reg_info = self.load_registration_info(
            self.registration_info_path)

        # Process exam plan columns
        self.course_name = self.load_course_name()
        self.course_num = self.load_course_num()
        self.semester = self.load_semester()
        self.number_of_students = self.load_number_of_students()
        self.start_date, self.end_date, self.splitted_df = self.split_date(self.exam_plan)
        self.exam_rooms = self.split_rooms(self.exam_plan)
        self.exam_form = self.load_exam_form()
        self.examiner = self.split_examiners(self.exam_plan)

        self.examiners, self.exam_date = self.split_examiners_exams(self.exam_plan)
        self.examiners_exams_df = self.create_examiners_exams_df()

    def load_exam_plan(self, exam_plan):
        return pd.read_excel(exam_plan)

    def load_room_distances(self, room_distances):
        return pd.read_excel(room_distances)

    def load_room_capacities(self, room_capacities):
        with open(room_capacities) as file:
            data = json.load(file)
        return data

    def load_special_dates(self, special_dates):
        return pd.read_csv(special_dates, delimiter=";")

    def load_special_examiners(self, special_examiners):
        return pd.read_excel(special_examiners)

    def split_examiners(self, dataframe):
        splitted_df = dataframe
        splitted_df['1. & 2. Pruefer'] = dataframe['1. & 2. Pruefer'].apply(
            lambda x: [examiner_row.strip() for examiner_row in x.split(',')])
        return splitted_df['1. & 2. Pruefer']

    def load_registration_info(self, registration_info):
        registration_info = pd.read_csv(registration_info)
        registration_info[['courseNumber', 'matnr']] = registration_info['courseNumber;matnr'].str.split(';',
                                                                                                         expand=True)

        # del the first columns that is 'courseNumber;matnr'
        registration_info = registration_info.drop('courseNumber;matnr', axis=1)
        # first column is the course number and each row is the students who takes it
        course_stud = registration_info.groupby('courseNumber')['matnr'].apply(list)
        # turns into data frame(courseNumber,matnr) and adds a column shows the index for each row by using reset index method
        course_stud = course_stud.to_frame().reset_index()

        return course_stud['courseNumber'], course_stud['matnr'], course_stud, registration_info

    def split_date(self, dataframe):
        splitted_df = dataframe
        splitted_df[['start_date', 'end_date']] = dataframe['Datum, Uhrzeit (ggf. sep. Zeitplan beachten)'].str.split(
            " - ", expand=True)
        splitted_df[['start_date', 'end_date']] = pd.to_datetime(splitted_df[['start_date', 'end_date']].stack(),
                                                                 format='%Y-%m-%dT%H:%M').unstack()

        return splitted_df['start_date'], splitted_df['end_date'], splitted_df

    def load_course_name(self):
        return self.exam_plan['Lehrveranstaltung']

    def load_course_num(self):
        return self.exam_plan['LV-Nr.']

    def load_semester(self):
        return self.exam_plan['Plansemester']

    def load_number_of_students(self):
        return self.exam_plan['Anzahl']

    def load_exam_form(self):
        return self.exam_plan['Form']

    def create_examiners_exams_df(self):
        return pd.merge(self.examiners, self.exam_date, left_index=True, right_index=True)

    def split_examiners_exams(self, dataframe):
        return dataframe['1. & 2. Pruefer'], dataframe['Datum, Uhrzeit (ggf. sep. Zeitplan beachten)']

    def split_rooms(self, rooms):
        # Remove leading and trailing whitespace and split by comma
        rooms['HS'] = rooms['HS'].apply(lambda x: [room.strip() for room in x.split(',')])
        self.room_distances.index = self.room_distances.columns
        return rooms['HS']
