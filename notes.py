"""
   
    Comment Line for the illia

    Input:
    a file contains just one columns as 'courseNumber;matnr'
    # That means we have exams and student who is taking this exam.
                
    Output:
    data frame has two columns as courseNumber, matnr
                
 
    '''
    exam_plan = pd.read_excel("datafiles/FIW_Exams_2022ws.xlsx")
    coursemat_df = pd.read_csv("datafiles/Pruefungsanmeldungen_anonmous.csv")

    # split into two columns
    coursemat_df[['courseNumber','matnr']] = coursemat_df['courseNumber;matnr'].str.split(';',expand=True)

    # del the first columns that is 'courseNumber;matnr'
    coursemat_df = coursemat_df.drop('courseNumber;matnr',axis=1)

    # first column is the course number and each row is the students who takes it
    course_stud = coursemat_df.groupby('courseNumber')['matnr'].apply(list)
    #turns into data frame(courseNumber,matnr) and adds a column shows the index for each row by using reset index method
    course_stud = course_stud.to_frame().reset_index()
    print(course_stud)
    #courseNumber -> LV-Nr
    course_stud.columns = ['LV-Nr.', 'matnr']
    # this column's type turns into the string from object
    course_stud['LV-Nr.'] = course_stud['LV-Nr.'].astype(str)
    # this column's type turns into the string from object
    exam_plan['LV-Nr.'] = exam_plan['LV-Nr.'].astype(str)
    #two table are merged via one common column.
    merged_df = pd.merge(exam_plan, course_stud, on='LV-Nr.')
    print(merged_df)
    merged_df['start_date'] = pd.to_datetime(merged_df['start_date'])
    print(merged_df)


-------------------------------


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

"""