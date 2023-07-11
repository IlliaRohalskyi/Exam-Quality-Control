import pandas as pd

def read_exam_plan():
    """
    Reads the exam plan(FIW_Exams_2022ws) from an Excel file and returns a pandas DataFrame.
    
    DataFrame consists of;
        Lehrveranstaltung: String
        LV-Nr.: String List
        Plansemester: String List
        Anzahl: Integer
        Datum, Uhrzeit (ggf. sep. Zeitplan beachten): String
        HS: String List
        Form: String List
        1. & 2. Pruefer: String List
    """
    try:
        filepath="datafiles/FIW_Exams_2022ws.xlsx"
        df = pd.read_excel(filepath, sheet_name=0)

        df['LV-Nr.'] = df['LV-Nr.'].astype(str)
        string_lists = ['LV-Nr.', 'Plansemester', 'HS','1. & 2. Pruefer']
        for string_list in string_lists:
            df[string_list] = df[string_list].str.split(",")

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
        return df
    except Exception as e:
        print(f"Error reading registration list: {str(e)}")
        return None

#to see the values of the dataraframes
print(read_exam_plan().values)
print(read_registration_list().values)
