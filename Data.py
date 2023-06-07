import pandas as pd
import json

exam_plan = "input_data_files/FIW_Exams_2022ws.xlsx"
registration_info = "input_data_files/Pruefungsanmeldungen_anonmous.csv"
room_distances = "input_data_files/room_distance_matrix.xlsx"
room_capacities = "input_data_files/capacity.json"
class Data:
    column_mapping = {
        'Lehrveranstaltung': 'course_name',
        'LV-Nr.': 'course_num',
        'Plansemester': 'semester',
        'Anzahl': 'student_num',
        'Datum, Uhrzeit (ggf. sep. Zeitplan beachten)': 'exam_date',
        'HS': 'exam_room',
        'Form': 'exam_form',
        '1. & 2. Pruefer': 'examiners'
    }


    def __init__(self):
        self.exam_plan = self.load_data(exam_plan)
        self.room_distances = self.load_room_distances(room_distances)
        self.room_capacities = self.load_room_capacities(room_capacities)
        self.course_name = None
        self.course_num = None
        self.semester = None
        self.student_num = None
        self.exam_date = None
        self.exam_room = None
        self.exam_form = None
        self.examiners = None
        self.start_date, self.end_date = self.split_date(self.exam_plan)
        self.course_nr, self.mat_nr, self.course_stud = self.registration_info(registration_info)
        self.extract_columns()

    def registration_info(self, registration_info):
        registration_info = pd.read_csv(registration_info)
        registration_info[['courseNumber','matnr']] = registration_info['courseNumber;matnr'].str.split(';',expand=True)

        # del the first columns that is 'courseNumber;matnr'
        registration_info = registration_info.drop('courseNumber;matnr',axis=1)
        # first column is the course number and each row is the students who takes it
        course_stud = registration_info.groupby('courseNumber')['matnr'].apply(list)
        #turns into data frame(courseNumber,matnr) and adds a column shows the index for each row by using reset index method
        course_stud = course_stud.to_frame().reset_index()
        
        return course_stud['courseNumber'], course_stud['matnr'], course_stud
    
    def load_data(self, exam_plan):
        return pd.read_excel(exam_plan)

    def extract_columns(self):
        columns = self.exam_plan.columns
        for column in columns:
            attribute_name = self.column_mapping.get(column, column)
            setattr(self, attribute_name, self.exam_plan[column])

    def load_room_distances(self, room_distances):
        return pd.read_excel(room_distances)

    def load_room_capacities(self, room_capacities):
            with open(room_capacities) as file:
                data = json.load(file)
            return data

    def split_date(self, dataframe):
        splitted_df = dataframe
        splitted_df[['start_date', 'end_date']] = dataframe['Datum, Uhrzeit (ggf. sep. Zeitplan beachten)'].str.split(" - ", expand = True)
        splitted_df[['start_date', 'end_date']] = pd.to_datetime(splitted_df[['start_date', 'end_date']].stack(), format='%Y-%m-%dT%H:%M').unstack()

        return splitted_df['start_date'], splitted_df['end_date']

input = Data()
course_name = input.course_name
course_num = input.course_num
semester = input.semester

print(input.course_stud)
