#import pandas as pd
#import numpy as np
#from datetime import datetime


import markdown
import pdfkit


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
    np.array object containing: 1. days difference; 2. student count; 3. exam name
    
    '''
    
    df = dataframe
    df['delta'] = (df.start_date - exam_start_date).dt.days
    
    
    conflict = df.loc[(df.delta>days_thresh) & (df.Anzahl>stud_thresh)]
    arr = np.array(conflict[['delta', 'Anzahl', 'Lehrveranstaltung']])
    
    score = float(len(conflict)/len(df))
    return score, arr
  
  #---------------------------------------------------#
  

  #---------------Output Processes-----------------------# 

example_data = {
    "courseName": ["Math"],
    "numberOfStudent": ["300"],
    "startDate": ["24.05.2023"],
    "endDate": ["24.06.2023"],
    "score": ["24.06.2023"]
}

def get_output(example_data, output_type):

    #initialize variables
    course_name = example_data['courseName']
    number_of_student = example_data['numberOfStudent']
    start_date = example_data['startDate']
    end_date = example_data['endDate']
    score = example_data['score']

    #create markdown text based on the coming data
    markdown_text = f""" 
# Exam Quality Control

## First Exam: 

- Name of the course: {course_name}  
- Number of students who enrolled this course: {number_of_student}
- Total Score: {score}


This exam should be helded on {start_date} - {end_date} based on this information
"""
    
        # converts the markdown text into html
    html = markdown.markdown(markdown_text)
        

    if output_type == 'html':

        file_directory = "output.html"

        #creates a file
        file = open(file_directory,"w",encoding="utf-8")

        file.write(html)
        print('Printing Process is successfully ended')

        file.close()
    
    elif output_type == 'pdf':

        path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

        html = markdown.markdown(markdown_text)
        path_to_file = 'output.html'

        #Point pdfkit configuration to wkhtmltopdf.exe
        # config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

        config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
        pdfkit.from_string(html, output_path='sample.pdf', configuration=config)

 
 
get_output(example_data,'pdf');
get_output(example_data,'html');


  #---------------------------------------------------#
