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
    
 
 
      total_score = scoring.one_exam_per_day.score * 0.22
     

      total_score += (scoring.one_day_gap.score * 0.20)  
      total_score += (scoring.special_dates.score * 0.18) 
      total_score += (scoring.big_exams_early.score * 0.16)  
      total_score += scoring.special_professors.score * 0.10
      total_score += scoring.room_capacity.score * 0.08
      total_score += (scoring.room_distances.score * 0.06)  

      html_body = "<div style='text-align: center;'>"
      html_body += "<h1 style='color: red;'>Total Score:</h1>"
      html_body += "<p style='color: red;'>" + str(total_score) + "</p>"
      html_body += "</div>"

      html_body += " <h3>Criteria for weighted scores:</h3>"
       
      html_body += '<p>' + 'one exam per day :' + str(scoring.one_exam_per_day.score) + '*' + str(0.22)  + ' = ' + str(scoring.one_exam_per_day.score * 0.22)   + '</p>'
      html_body += '<p>' + 'one day gap :' + str(scoring.one_day_gap.score) + '*' + str(0.20)  + ' = ' +  str((scoring.one_day_gap.score * 0.20))  + '</p>'
      html_body += '<p>' + 'special dates :' +  str(scoring.special_dates.score) + '*' + str(0.18) + ' = ' +  str((scoring.special_dates.score * 0.18)) + '</p>'
      html_body += '<p>' + 'big exams early :' +  str(scoring.big_exams_early.score) + '*' + str(0.16) + ' = ' +  str((scoring.big_exams_early.score * 0.16)) + '</p>'
      html_body += '<p>' + 'special professors :' +  str(scoring.special_professors.score) + '*' + str(0.10) + ' = ' +  str( scoring.special_professors.score * 0.10) + '</p>'
      html_body += '<p>' + 'room capacity :' +  str(scoring.room_capacity.score) + '*' + str(0.08) + ' = ' +  str(scoring.room_capacity.score * 0.08) + '</p>'
      html_body += '<p>' + 'room distances :' +  str(scoring.room_distances.score) + '*' + str(0.06) + ' = ' +  str(scoring.room_distances.score * 0.06) + '</p>'
      html_body += '<hr>';
 
      

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

        html_body += HtmlConverter.create_html_body(table,score,graph,obj_name) 
       

      return html_body
           
    @staticmethod
    # Use to save your multiple_results as html
    def save_multiple_result_html():
        
           
        html_body=Output._create_html_multiple_result_body()   
        html_page=HtmlConverter.create_html_page(html_body)
        HtmlConverter.print_html_output(html_page,"result_list.html")

    @staticmethod
    def _create_html_single_result_body(name=None):
        html_body = ""

        for obj_name, obj in scoring.__dict__.items():
            if name is not None and obj_name != name:
                continue

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

            result = HtmlConverter.create_html_body(table, score, graph, obj_name)
            html_body += result  # Her sonucu doğrudan html_body'ye ekliyoruz

        return html_body

    @staticmethod
    def save_single_result_html(name=None):
        html_body = Output._create_html_single_result_body(name)
        html_page = HtmlConverter.create_html_page(html_body)
        filename = name + ".html"
        HtmlConverter.print_html_output(html_page, filename)

#######################################################

    
