from Output import Output

def main():


    Output.save_multiple_result_html()
    
    Output.save_single_result_html("one_exam_per_day") # 0.22
    Output.save_single_result_html("one_day_gap") # 0.20
    Output.save_single_result_html("special_dates") # 0.18
    Output.save_single_result_html("big_exams_early") # 0.16
    Output.save_single_result_html("special_professors") # 0.10
    Output.save_single_result_html("room_capacity") # 0.08
    Output.save_single_result_html("room_distances") # 0.06



main()
