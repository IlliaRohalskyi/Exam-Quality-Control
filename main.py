
import markdown


# Output Processes

def getOutput(courseName, numberOfStudent,date):

    markdownText = f""" 
# Exam Plan Quality

## First Exam: 

### Name of the course: {courseName}  
### the number of students who enrolled this course: {numberOfStudent}

This exam should be helded on {date} based on this information
"""

    # converts the markdown text into html
    html = markdown.markdown(markdownText)

    file_directory = "output.html"

    #creates a file
    file = open(file_directory,"w",encoding="utf-8")

    file.write(html)
    print('Printing Process is successfully ended')

    file.close()
 
getOutput('Math',300
,24.05);