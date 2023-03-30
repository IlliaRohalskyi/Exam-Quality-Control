import pandas as pd
import numpy as np
from datetime import datetime
import markdown

#--------------------Processing functions--------------------#

def split_date(dataframe):
    '''
    Input:
    dataframe: exam dataframe with type pandas.core.frame.DataFrame
    
    Output:
    pandas.core.frame.Dataframe with splitted date in two new columns:
                            'start_date', 'end_date' with dtype datetime64[ns]
    
    '''
    splitted_df = dataframe
    splitted_df[['start_date', 'end_date']] = dataframe['Datum, Uhrzeit (ggf. sep. Zeitplan beachten)'].str.split(" - ", expand = True)
    splitted_df[['start_date', 'end_date']] = pd.to_datetime(splitted_df[['start_date', 'end_date']].stack(), format='%Y-%m-%dT%H:%M').unstack()
    
    return splitted_df

def big_exams_early(dataframe, days_thresh, stud_thresh, exam_start_date):
    '''
    
    Input: 
    dataframe: Exam dataframe with type pandas.core.frame.DataFrame. It must be splitted with split_date function beforehand
    days_thresh: Days threshold, type int
    stud_thresh: Student count threshold, type int
    exam_start_date: date of the official exam start, type datetime64[ns]
    
    Output: 
    Score with type float
    
    '''
    
    df = dataframe
    delta = df.start_date - exam_start_date
    df.delta = delta.astype(int)
    
    
    conflict = dataframe.loc[(dataframe.delta>days_thresh) & (dataframe.Anzahl>stud_thresh)]
    
    score = float(len(conflict)/len(df))
    return score
  
  #---------------------------------------------------#
  
  
# Output Processes

def getOutput(courseName, numberOfStudent,date):

    markdownText = f""" 
# Exam Plan Quality

## First Exam: 

### Name of the course: {courseName}  
### the number of students who enrolled this course: {numberOfStudent}

This exam should be helded on {date} based on this information
"""

    # converts the markdown text into html
    html = markdown.markdown(markdownText)

    file_directory = "output.html"

    #creates a file
    file = open(file_directory,"w",encoding="utf-8")

    file.write(html)
    print('Printing Process is successfully ended')

    file.close()
 
getOutput('Math',300
,24.05);


