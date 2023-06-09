import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import markdown
import pdfkit
from datetime import datetime
from Data import Data
from HtmlConverter import HtmlConverter
from OneExamPerDay import OneExamPerDay
from Scoring import scoring
from Output import Output
from Data import data_obj


def main():

    # Output.save_multiple_result_html()
    # Output.save_result_bigExamEarly()
    Output.save_result_oneExamPerDay()
    # Output.save_result_roomCapacity()
    # Output.save_result_roomDistances()

main()