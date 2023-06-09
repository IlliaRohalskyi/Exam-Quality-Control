import pandas as pd
import json
from HtmlConverter import HtmlConverter
from Scoring import scoring




class Output:



    def __init__(self):
        pass
        

    # Don't call it because it is just a helper class
    @staticmethod
    def _create_html_multiple_result_body():
    
      html_body = ""
      
      for obj_name, obj in scoring.__dict__.items():

        if obj.conflicts_df is not None:
          table = HtmlConverter.add_table(obj.conflicts_df)
        else:
          table = ""

        if obj.score is not None:
          score = HtmlConverter.add_score(obj.score)
        else:
          score = ""  

        if obj.plot_arr is not None:
          graph = HtmlConverter.add_graph(obj.plot_arr)
        else:
          graph = ""  

        html_body = HtmlConverter.create_html_body(table,score,graph,obj_name) 
       

      return html_body
           


    @staticmethod
    # Use to save your multiple_results as html
    def save_multiple_result_html():
           
        html_body=Output._create_html_multiple_result_body()   
        html_page=HtmlConverter.create_html_page(html_body)
        HtmlConverter.print_html_output(html_page,"result.html")

#######################################################

    
 # Don't call it because it is just a helper class
    @staticmethod
    def _create_html_single_result_body(obj):
    
      html_body = ""
      

      if obj.conflicts_df is not None:
        table = HtmlConverter.add_table(obj.conflicts_df)
      else:
        table = ""
      if obj.score is not None:
        score = HtmlConverter.add_score(obj.score)
      else:
        score = ""  
      if obj.plot_arr is not None:
        graph = HtmlConverter.add_graph(obj.plot_arr)
      else:
        graph = ""  
      html_body = HtmlConverter.create_html_body(table,score,graph,obj.__class__.__name__) 
      

      return html_body
           

    @staticmethod
        # Use to save your multiple_results as html
    def save_result_bigExamEarly():
              
            html_body=Output._create_html_single_result_body(scoring.big_exams_early)   
            html_page=HtmlConverter.create_html_page(html_body)
            HtmlConverter.print_html_output(html_page,"bigExamEarly.html")
    @staticmethod
        # Use to save your multiple_results as html
    def save_result_roomCapacity():
              
            html_body=Output._create_html_single_result_body(scoring.room_capacity)   
            html_page=HtmlConverter.create_html_page(html_body)
            HtmlConverter.print_html_output(html_page,"roomCapacity.html")
    @staticmethod
        # Use to save your multiple_results as html
    def save_result_roomDistances():
              
            html_body=Output._create_html_single_result_body(scoring.room_distances)   
            html_page=HtmlConverter.create_html_page(html_body)
            HtmlConverter.print_html_output(html_page,"roomDistances.html")
    @staticmethod
        # Use to save your multiple_results as html
    def save_result_oneExamPerDay():
              
            html_body=Output._create_html_single_result_body(scoring.one_exam_per_day)   
            html_page=HtmlConverter.create_html_page(html_body)
            HtmlConverter.print_html_output(html_page,"oneExamPerDay.html")

