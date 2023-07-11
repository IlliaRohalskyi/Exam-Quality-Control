import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import markdown
import pdfkit
from datetime import datetime


class utilities:

    def __init__(self, df, model, year, color):
            self.brand = brand
            self.model = model
            self.year = year
            self.color = color
            self.current_speed = 0
            
    
    def read_data():

        df=pd.read_excel("datafiles/FIW_Exams_2022ws.xlsx")
        return df