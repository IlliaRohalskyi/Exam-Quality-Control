import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import markdown
import pdfkit
from datetime import datetime


def main():

    dataframe = read_data()
    splitted_df = split_date(dataframe)
    sorted_df = splitted_df.sort_values(by='start_date')
    exam_start_date=sorted_df.loc[0,'start_date']
    print(exam_start_date)
    score,conflicts_df = big_exams_early(splitted_df)
    get_output(conflicts_df,score,'html');

def read_data():

    df=pd.read_excel("datafiles/FIW_Exams_2022ws.xlsx")
    return df
  
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

def big_exams_early(splitted_df):
    '''
    
    Input: 
    splitted_df: Exam dataframe with type pandas.core.frame.DataFrame. It must be splitted with split_date function beforehand
    
    Output: 
    Score with type float
    np.array object containing: 1. days difference; 2. student count; 3. exam name
    saves a plot with file name big_exams_early.png
    
    '''
    
    df = splitted_df
    
    sorted_date = df.sort_values(by='start_date')
    exam_start_date = sorted_date.loc[0,'start_date']
    
    df['delta'] = (df.start_date - exam_start_date).dt.days
    
    subjects_sorted = df.sort_values('Anzahl', ascending=False)
    latest_day = df['delta'].max()
    
    stud_counts = np.array(subjects_sorted.Anzahl)
    timeline = np.linspace(0, latest_day, num=len(stud_counts))
    
    ### Compute dots ###
    
    dots = {0: stud_counts[0]}
    for i in range(1, latest_day+1):
        diff = np.abs(timeline - i)
        sorted_indices = np.argsort(diff)

        index1 = sorted_indices[0]
        index2 = sorted_indices[1]
        
        t = (i - timeline[index1])/(timeline[index2]-timeline[index1])
        
        y = (1-t) * stud_counts[index1] + t * stud_counts[index2]
        
        dots[i] = y
        
    ### Compute score ###
    
    neg_score = 0
    arr = []
    for row in df.itertuples():
        if row.Anzahl > dots[row.delta]:
            neg_score = neg_score + np.abs(row.Anzahl - dots[row.delta])
            arr.append([row.delta, row.Anzahl, row.Lehrveranstaltung])
    arr = np.array(arr)
    worst_score = np.sum(df.Anzahl) - np.min(stud_counts)
    score = 1 - neg_score/worst_score
    
    ### Create plot ###
    
    plt.figure(figsize=(15, 10))
    plt.plot(timeline, stud_counts)
    
    dots_y = np.array(arr[:, 1], dtype=int)
    dots_x = np.array(arr[:, 0], dtype=int)
    subj_names = arr[:, 2]
    plt.scatter(dots_x, dots_y, s=10, color='red')
    
    for i in range(len(dots_x)):
        plt.text(dots_x[i], dots_y[i], subj_names[i], fontsize=6)
    plt.title('Big exams early conflicts')
    plt.xlabel('Day')
    plt.ylabel('Student count')
    plt.savefig('big_exams_early.png')
    
    ### Reformat conflict array to dataframe, return score and conflict dataframe ###
    
    conflicts_df = pd.DataFrame(arr, columns=['days_diff', 'stud_count', 'exam_name'])
    return score, conflicts_df
  
  #---------------------------------------------------#



  

  #---------------Output Processes-----------------------# 


def get_output(example_data,score,output_type):



    

    # create markdown text based on the coming data
    # in case that we need mark down again
    # markdown_text = f""" """

    # converts the markdown text into html
    # html = markdown.markdown(markdown_text)
    
    html= '''

    <html>
    <head>
    </head>
    <body>
      <main >
    <h1 style="text-align:center">Exam Quality Control</h1>

    <div style="margin: auto;width: 1200px;display: flex;gap:6rem;justify-content: center;">
        <div>
            <h2>Lists of Conflicts:</h2>

            <table style=" border: 1px solid;  border-collapse: collapse;">
                <tr>
                    <th>Day</th>
                    <th>Student Count</th>
                    <th>Exam Name</th>
                </tr>
        
    
    '''



    for i in range(len(example_data['days_diff'])):

      

        days = example_data.loc[i,'days_diff']
        student_count = example_data.loc[i,'stud_count']
        exam_name = example_data.loc[i,'exam_name']
    

        data = { "day": days, "student_count": student_count,"exam_name": exam_name}
        html += "  <tr style=\" text-align:center; \" > \n <td style=\" padding: 1rem \" >{day}</td> \n <td>{student_count}</td> \n <td>{exam_name}</td> \n </tr>  \n ".format(**data)



    html += '''
       
    </table>
    </ul>
 
    </div>
    <div style="margin-top: 4rem">
    <img src="./Thws-logo_English.png" style=" width: 400px" alt="big exams early">
    </div>
    </div>
    <img src="./big_exams_early.png"  alt="big exams early">
    </main>
    </body>
    </html>
    '''

  
    
  



    if output_type == 'html':

        file_directory = "output.html"

        #creates a file
        file = open(file_directory,"w",encoding="utf-8")

        file.write(html)
        print('Printing Process is successfully ended')

        file.close()
    
    elif output_type == 'pdf':

          # in case that we need pdf again
   
        path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

        html = markdown.markdown(markdown_text)
        path_to_file = 'output.html'

        #Point pdfkit configuration to wkhtmltopdf.exe
        # config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

        config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
        pdfkit.from_string(html, output_path='sample.pdf', configuration=config)


if __name__ == '__main__':
    main()
