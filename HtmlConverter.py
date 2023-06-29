import matplotlib.pyplot as plt
import io
import base64
import numpy as np 

class HtmlConverter:
   
    def __init__(self):
           pass
      
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
        
        html = " <h3 style=\"text-align:center\">Score:</h3>"
       
        html += '<p>'
        html += str(score)
        html += '</p>' 
      
        return html


    @staticmethod
    def add_graph(plot_arr):
       # Convert the plot array to an image
        buf = io.BytesIO()
        plt.imsave(buf, plot_arr, format='png')
        buf.seek(0)
        plot_data = base64.b64encode(buf.read()).decode('utf-8')

        # Embed the image in an HTML string
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
            <h2>Lists of Conflicts:</h2>

           
               
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
        
        file_directory = "./outputs/"  
        file_directory += file_name

    
        file = open(file_directory, "w", encoding="utf-8")
        file.write(html)
        file.close()
    
   

