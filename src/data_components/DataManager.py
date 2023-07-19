from data_components.Data import Data


class DataManager:
    def __init__(self):
        self.data_instance = None

    def get_data_instance(self, exam_plan_path=None, registration_info_path=None, room_distances_path=None,
                          room_capacities_path=None, special_dates_path=None, special_examiner_path=None):
        if self.data_instance is None:
            self.data_instance = Data(exam_plan_path, registration_info_path, room_distances_path,
                                      room_capacities_path, special_dates_path, special_examiner_path)
        return self.data_instance

    @staticmethod
    def create_mock_data_instance(mock_exam_plan_path, mock_registration_info_path, mock_room_distances_path,
                                  mock_room_capacities_path, mock_special_dates_path, mock_special_examiner_path):
        return Data(mock_exam_plan_path, mock_registration_info_path, mock_room_distances_path,
                    mock_room_capacities_path, mock_special_dates_path, mock_special_examiner_path)
