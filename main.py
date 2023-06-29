import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import markdown
from SpecialDates import SpecialDates  # special_dates yerine SpecialDates kullanın
import pdfkit
from datetime import datetime
from Data import Data
from HtmlConverter import HtmlConverter
from OneExamPerDay import OneExamPerDay
from Scoring import scoring
from Output import Output
from Data import data_obj

def main():


    Output.save_multiple_result_html()
    Output.save_single_result_html("big_exams_early")
    Output.save_single_result_html("one_exam_per_day") 
    Output.save_single_result_html("room_distances") 
    Output.save_single_result_html("room_capacity")

    # special_dates = SpecialDates()  # SpecialDates sınıfından bir örnek oluşturun
    # score, conflicts_df, plot_arr = special_dates.compute()  # compute yöntemini çağırın

    # print(score, conflicts_df)  # Sonuçları yazdırın

main()
