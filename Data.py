import pandas as pd
import json

exam_plan = "input_data_files/FIW_Exams_2022ws.xlsx"
registration_info = "input_data_files/Pruefungsanmeldungen_anonmous.csv"
room_distances = "input_data_files/room_distance_matrix.xlsx"
room_capacities = "input_data_files/capacity.json"
special_dates = "input_data_files/special_dates.csv"
special_examiner = "input_data_files/specific_professors.xlsx"
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
        # self.exam_date = None
        self.exam_room = self.split_rooms(self.exam_plan)
        self.exam_form = None
        self.examiners = self.split_examiners(self.exam_plan)
        self.start_date, self.end_date, self.splitted_df = self.split_date(self.exam_plan)
        self.course_nr, self.mat_nr, self.course_stud, self.reg_info = self.registration_info(registration_info)
        self.examiners,self.exam_date = self.split_examiners_exams(self.exam_plan)
        self.special_dates_df = self.load_special_dates()
        self.examiners_exams_df = self.create_examiners_exams_df()
        self.special_examiners = self.load_special_examiners(self)

        self.extract_columns()

    def load_special_examiners(self,special_examiners):
        return pd.read_excel(special_examiners)

    
    def registration_info(self, registration_info):
        registration_info = pd.read_csv(registration_info)
        registration_info[['courseNumber','matnr']] = registration_info['courseNumber;matnr'].str.split(';',expand=True)

        # del the first columns that is 'courseNumber;matnr'
        registration_info = registration_info.drop('courseNumber;matnr',axis=1)
        # first column is the course number and each row is the students who takes it
        course_stud = registration_info.groupby('courseNumber')['matnr'].apply(list)
        #turns into data frame(courseNumber,matnr) and adds a column shows the index for each row by using reset index method
        course_stud = course_stud.to_frame().reset_index()
        
        return course_stud['courseNumber'], course_stud['matnr'], course_stud, registration_info


    def extract_columns(self):
        columns = self.exam_plan.columns
        for column in columns:
            attribute_name = self.column_mapping.get(column, column)
            setattr(self, attribute_name, self.exam_plan[column])


    def load_data(self, exam_plan):
        return pd.read_excel(exam_plan)

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

        return splitted_df['start_date'], splitted_df['end_date'], splitted_df
    
    def load_special_dates(self):
          return pd.read_csv(special_dates, delimiter=";")
    
    def create_examiners_exams_df(self):
        return pd.merge(self.examiners, self.exam_date, left_index=True, right_index=True)

    def split_examiners_exams(self, dataframe):
        return dataframe['1. & 2. Pruefer'],dataframe['Datum, Uhrzeit (ggf. sep. Zeitplan beachten)']


    def split_rooms(self,rooms):
        # Remove leading and trailing whitespace and split by comma
        rooms['HS'] = rooms['HS'].apply(lambda x: [room.strip() for room in x.split(',')])
        self.room_distances.index=self.room_distances.columns

    def split_examiners(self, dataframe):
        splitted_df = dataframe
        splitted_df['1. & 2. Pruefer'] = dataframe['1. & 2. Pruefer'].apply(
            lambda x: [examiner_row.strip() for examiner_row in x.split(',')])
        return splitted_df
        
        
data_obj = Data()