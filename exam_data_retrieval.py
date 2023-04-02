import pandas as pd

def read_exam_plan():
    """
    Reads the exam plan(FIW_Exams_2022ws) from an Excel file and returns a pandas DataFrame.
    """
    try:
        filepath="datafiles/FIW_Exams_2022ws.xlsx"
        df = pd.read_excel(filepath, sheet_name=0)
        df.columns = ["course_name", "course_number", "semester", "number_of_exams", "date", "location", "format", "examiner"]
        df['course_number'] = df['course_number'].astype(str)
        str_vars = ["course_number", "semester", "date", "location", "examiner"]
        for var in str_vars:
            df[var] = df[var].str.split(",")
        return df
    except Exception as e:
        print(f"Error reading exam plan: {str(e)}")
        return None

def read_registration_list():
    """
    Reads the registration list (Pruefungsanmeldungen_anonmous) from a CSV file and returns a pandas DataFrame.
    """
    try:
        filepath = "datafiles/Pruefungsanmeldungen_anonmous.csv"
        df = pd.read_csv(filepath, sep=";")
        df.columns = ["course_number", "student_id"]
        return df
    except Exception as e:
        print(f"Error reading registration list: {str(e)}")
        return None
    
