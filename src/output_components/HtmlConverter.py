import matplotlib.pyplot as plt
import io
import base64
import os
from rule_components.Scoring import scoring

class HtmlConverter:
   
    def __init__(self):
           pass
      


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
            html_body += result

        return html_body


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
    def create_html_body(table,score,graph,rule_name):
             
        html_multiple_result_body = '<div>' + " <h1> " + rule_name + "</h1>" + table + score + graph + '</div>'

        return  html_multiple_result_body
    
    @staticmethod
    def add_table(required_df):
        html = " <hr> " 
        html += "<table style=\" border: 1px solid;  border-collapse: collapse;\">"
       
        html += '<tr>'
        for col_name in required_df.columns:
            html += f'<th>{col_name}</th>'
        html += '</tr>'

        
        for i in range(len(required_df)):
            html += '<tr style="text-align:center;">'
            for j in range(len(required_df.columns)):
                cell_data = required_df.iloc[i, j]
                html += f'<td style="padding:1rem">{cell_data}</td>'
            html += '</tr>'

        html += "</table>"
        return html
    @staticmethod
    def add_score(score):
        
        html = " <h3>Score:</h3>"
       
        html += '<p>'
        html += str(score)
        html += '</p>' 
      
        return html


    @staticmethod
    def add_graph(plot_arr):

        buf = io.BytesIO()
        plt.imsave(buf, plot_arr, format='png')
        buf.seek(0)
        plot_data = base64.b64encode(buf.read()).decode('utf-8')


        html = f"<hr><img src='data:image/png;base64,{plot_data}'><hr>"
        

        return html
    @staticmethod
    def create_html_page(html_body):
        
        html = ""

        html= '''
        <html>
        <head>
        </head>
        <body>
        <main >
        <h1 style="text-align:center">Exam Quality Control</h1>

        <div style="margin: auto;width: 1200px;display: flex;gap:6rem;justify-content: center;">
            <div>
           

           
               
        '''
        
        html += html_body

        html += '''
             </table>
       
        </div>
        <div style="margin-top: 4rem">
       
        </div>
        </div>
   
        </main>
        </body>
        </html>
        '''
        
        return html
    
    @staticmethod
    def print_html_output(html_page,file_name):

        html = html_page
        
        file_directory = os.path.dirname(os.path.abspath(__file__))
        file_directory += file_name

    
        file = open(file_directory, "w", encoding="utf-8")
        file.write(html)
        file.close()
    
   

