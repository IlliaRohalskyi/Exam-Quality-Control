from Data import Data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from RoomCapacity import RoomCapacity
from RoomDistance import RoomDistance
from BigExamsEarly import BigExamsEarly
from OneExamPerDay import OneExamPerDay

data_obj = Data()
class Scoring():
    def __init__(self):
        self.big_exams_early = BigExamsEarly()
        self.one_exam_per_day = OneExamPerDay()
        self.room_capacity = RoomCapacity()
        self.room_distances = RoomDistance()
        
scoring = Scoring()