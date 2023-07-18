import pandas as pd
import json
from src.HtmlConverter import HtmlConverter
from src.Scoring import scoring




class Output:



    def __init__(self):
        pass
       
           
    @staticmethod
    # Use to save your multiple_results as html
    def save_multiple_result_html():
        
           
        html_body=HtmlConverter._create_html_multiple_result_body()   
        html_page=HtmlConverter.create_html_page(html_body)
        HtmlConverter.print_html_output(html_page,"result_list.html")



    @staticmethod
    def save_single_result_html(name=None):
        html_body = HtmlConverter._create_html_single_result_body(name)
        html_page = HtmlConverter.create_html_page(html_body)
        filename = name + ".html"
        HtmlConverter.print_html_output(html_page, filename)

#######################################################

    
