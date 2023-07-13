from Data import Data


class Rule:

    exam_plan_path = "input_data_files/FIW_Exams_2022ws.xlsx"
    registration_info_path = "input_data_files/Pruefungsanmeldungen_anonmous.csv"
    room_distances_path = "input_data_files/room_distance_matrix.xlsx"
    room_capacities_path = "input_data_files/capacity.json"
    special_dates_path = "input_data_files/special_dates.csv"
    special_examiner_path = "input_data_files/specific_professors.xlsx"

    data_obj = Data(exam_plan_path, registration_info_path, room_distances_path, room_capacities_path, special_dates_path,
                    special_examiner_path)

    def __init__(self):
        score, conflicts_df, plot_array = self.compute()

    def compute(self):
        return None, None, None
