import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Data import data_obj

class RuleEight:
    def __init__(self):
        self.score, self.conflicts_df, self.plot_arr = self.compute()

    def compute(self):
        score=None
        conflicts_df=None
        plot_arr= None
        def specific_examiners():
            df = pd.concat([data_obj.examiner,data_obj.start_date,data_obj.course_name],axis=1)
            exploded_df = df.explode('1. & 2. Pruefer')
            grouped_df = exploded_df.groupby('1. & 2. Pruefer').agg(
                {'Lehrveranstaltung': list, 'start_date': list}).reset_index()


            print(grouped_df)
        specific_examiners()
        return score, conflicts_df, plot_arr




RuleEight = RuleEight()
