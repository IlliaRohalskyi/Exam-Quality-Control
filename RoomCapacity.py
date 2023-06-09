import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Data import data_obj
class RoomCapacity:
    def __init__(self):
        self.score, self.plot_arr = self.compute()
        self.conflicts_df = None
    def compute(self):
        course_stud = data_obj.course_stud
        course_stud.columns = ['coursenr', 'matnr']
        # this column's type turns into the string from object
        course_stud['coursenr'] = course_stud['coursenr'].astype(str)
        # this column's type turns into the string from object
        exam_plan = data_obj.exam_plan.rename(columns={'LV-Nr.': 'coursenr'})
        exam_plan['coursenr'] = exam_plan['coursenr'].astype(str)

        #two table are merged via one common column.
        merged_df = pd.merge(exam_plan[['coursenr', 'HS']], course_stud, on='coursenr')

        merged_df['total_student'] = merged_df['matnr'].apply(lambda x: len(x))

        def calculate_total_capacity(row):


            import json

            # Read the json
            capacity = data_obj.room_capacities
        
            # reaching the room which you want to access
            rooms = capacity['Exam-room-capacities']
            room = None
        
            total = 0
            for i in row['HS']:
                for s in rooms.values():
                    for r in s:
                        if r['Name'] == i:
                            room = r
                            total = total + max(room['Klausur-capacity 1'], room['Klausur-capacity 2'])
                        
                    
                    if room:
                        break

            # Receiving total capacity
            return total
        
        # call the function for each row and add the result to a new column
        merged_df['Total Capacity'] = merged_df.apply(calculate_total_capacity, axis=1)

        x = merged_df['total_student'].values
        y = merged_df['Total Capacity'].values
        neg_score = 0
        worst_case = 0
        for i in range(len(x)):
            neg_score += abs(x[i]-y[i])
            worst_case += max(x[i], y[i])
        score = 1 - neg_score/worst_case
        plt.scatter(x, y)

        # draw the line
        fit_fn = np.poly1d([1, 0])
        plt.plot(x, fit_fn(x), '--k')
        plt.xlabel("Student")
        plt.ylabel("Capacity")
        plt.title("Room Capacity")
        # Convert the plot to a NumPy array
        figure = plt.gcf()  # Get the current figure
        figure.canvas.draw()  # Render the plot

        # Convert the plot to a NumPy array
        plot_array = np.array(figure.canvas.renderer.buffer_rgba())
        plt.show()
        plt.close()

        return score, plot_array
    
    