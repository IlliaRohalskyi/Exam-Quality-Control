import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.Rule import Rule
class OneExamPerDay(Rule):
    def __init__(self):
        super().__init__()
        self.score, self.conflicts_df, self.plot_arr = self.compute()
    def compute(self):
        def f(x):
            return (1/2) ** (x/(5*1000/self.data_obj.reg_info['matnr'].nunique()))
        
        course_stud = self.data_obj.course_stud
        course_stud.columns = ['coursenr', 'matnr']
        # this column's type turns into the string from object
        course_stud['coursenr'] = course_stud['coursenr'].astype(str)
        # this column's type turns into the string from object
        exam_plan = self.data_obj.splitted_df.rename(columns={'LV-Nr.': 'coursenr'})
        exam_plan['coursenr'] = exam_plan['coursenr'].astype(str)

        #two table are merged via one common column.
        merged_df = pd.merge(exam_plan, course_stud, on='coursenr')
        merged_df['start_date'] = pd.to_datetime(merged_df['start_date'])
        merged_df['date'] = merged_df['start_date'].dt.date
        
        
        # Create a dictionary to store the conflicts
        conflicts = {}
        # Loop through each row of the dataframe
        for i, row in merged_df.iterrows():
            # Get the date and students for the current row
            date = row['date']
            students = row['matnr']
            # Check if any of the students have already been seen on the same date
            for student in students:
                if student in conflicts and date in conflicts[student]:
                    # If the student is already in the conflicts dictionary for the current date,
                    # add the current exam name to the list of conflicting exams for the student
                    conflicts[student][date].append(row['Lehrveranstaltung'])
                elif student in conflicts:
                    # If the student is already in the conflicts dictionary but not for the current date,
                    # add the current date and exam name to the conflicts dictionary for the student
                    conflicts[student][date] = [row['Lehrveranstaltung']]
                else:
                    # If the student is not yet in the conflicts dictionary, add the student and
                    # the current date and exam name to the conflicts dictionary
                    conflicts[student] = {date: [row['Lehrveranstaltung']]}

        # Create a new dataframe to store the conflicts
        conflicts_df = pd.DataFrame(columns=['student_id', 'exam_names', 'date'])

        # Loop through each student in the conflicts dictionary
        for student, dates in conflicts.items():
            # Loop through each date for the student
            for date, exams in dates.items():
                # If the student has more than one exam on the date, add a row to the conflicts dataframe
                if len(exams) > 1:
                    conflicts_df = conflicts_df._append({
                        'student_id': student,
                        'exam_names': exams,
                        'date': date
                    }, ignore_index=True)
        conflicts_amount = len(conflicts_df)
        print(conflicts_amount)
        print(f(conflicts_amount))
        score = f(conflicts_amount)
        x_values = np.linspace(0, conflicts_amount+30, 1000)  
        y_values = f(x_values)

        plt.plot(x_values, y_values)
        plt.scatter(conflicts_amount, score, color='red')  # Add a red dot at the specified value
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('One Exam Per Day')
        plt.legend()
        plt.text(conflicts_amount, score, score, ha='right', va='bottom')
        
        # Convert the plot to a NumPy array
        figure = plt.gcf()  # Get the current figure
        figure.canvas.draw()  # Render the plot

        # Convert the plot to a NumPy array
        plot_array = np.array(figure.canvas.renderer.buffer_rgba())
        plt.show()
        plt.close()

        percentage_score = score * 100
        return percentage_score, conflicts_df, plot_array
