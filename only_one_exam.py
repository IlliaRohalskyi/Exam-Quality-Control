import pandas as pd
import numpy as np

enr_data = pd.read_csv("datafiles/Pruefungsanmeldungen_anonmous.csv")

# first we need to group our data by student number
# then, convert to a dict - matnr:key courseNumber:list of values

std_exams = enr_data.groupby('matnr')['courseNumber']\
    .apply(list).to_dict()









