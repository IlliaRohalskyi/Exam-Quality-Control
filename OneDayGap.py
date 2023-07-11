import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Data import data_obj
pd.set_option('display.max_columns', 20)

class OneDayGap:
    def __init__(self):
        self.score, self.conflicts_df, self.plot_arr = self.compute()
    def compute(self):
        def f(x):
            return (1/2) ** (x/(5*1000/data_obj.reg_info['matnr'].nunique()))
        
        def compare(list1, list2):
            common_values = []
            
            for item in list1:
                if item in list2:
                    common_values.append(item)
            
            return common_values
        
        course_stud = data_obj.course_stud
        course_stud.columns = ['coursenr', 'matnr']
        # this column's type turns into the string from object
        course_stud['coursenr'] = course_stud['coursenr'].astype(str)
        # this column's type turns into the string from object
        exam_plan = data_obj.splitted_df.rename(columns={'LV-Nr.': 'coursenr'})
        exam_plan['coursenr'] = exam_plan['coursenr'].astype(str)

        # two tables are merged via one common column.
        merged_df = pd.merge(exam_plan, course_stud, on='coursenr')
        merged_df['start_date'] = pd.to_datetime(merged_df['start_date'])
        merged_df['date'] = merged_df['start_date'].dt.date
       
        conflicts_df = pd.DataFrame({}, columns=['student_id', 'exam_names', 'dates'])
        merged_df.sort_values(by='date', ascending=True)
        for i, row1 in merged_df.iterrows():
            for j, row2 in merged_df.iterrows():
                if (row2.date - row1.date).days != 1:
                    continue
                no_gap_students = compare(row1['matnr'], row2['matnr'])
                if no_gap_students == []:
                    continue
                for stud in no_gap_students:
                    new_row = {'student_id': stud,
                               'exam_names': [[row1['Lehrveranstaltung'], row2['Lehrveranstaltung']]],
                               'dates': [[row1['date'], row2['date']]]}
                    conflicts_df = pd.concat([conflicts_df, pd.DataFrame(new_row)], ignore_index=True)                    
        conflicts_amount = float(len(conflicts_df))
        print(conflicts_amount)
        score = f(conflicts_amount)
        x_values = np.linspace(0, conflicts_amount+10, 1000)  
        y_values = f(x_values)

        plt.plot(x_values, y_values)
        plt.scatter(conflicts_amount, score, color='red')  # Add a red dot at the specified value
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('One Day Gap')
        plt.legend()
        plt.text(conflicts_amount, score, score, ha='right', va='bottom')
        
        # Convert the plot to a NumPy array
        figure = plt.gcf()  # Get the current figure
        figure.canvas.draw()  # Render the plot

        # Convert the plot to a NumPy array
        plot_array = np.array(figure.canvas.renderer.buffer_rgba())
        plt.show()
        plt.close()

        percantage_score = score
        return percantage_score , conflicts_df, plot_array