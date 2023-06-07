class RoomCapacity:
    def __init__(self, Data):
        self.score = None
        self.plot = None
        self.conflict_df = None
        def compute(self, Data):
            #two table are merged via one common column.
            merged_df = pd.merge(exam_plan[['LV-Nr.', 'HS']], course_stud, on='LV-Nr.')

            merged_df['total_student'] = merged_df['matnr'].apply(lambda x: len(x))

            def calculate_total_capacity(row):


                import json

                # Read the json
                with open('./datafiles/capacity.json') as f:
                    capacity = json.load(f)
                
                # Receive the strings in HS column and split them according to ,
                elements = row['HS'].split(', ')
            
                # reaching the room which you want to access
                rooms = capacity['Exam-room-capacities']
                room = None
            
                total = 0;
                for i in elements:
                    for s in rooms.values():
                        for r in s:
                            if r['Name'] == i:
                                room = r
                                # if you change this part you can also receive other capacities as well
                                total = total + room['Klausur-capacity 2']
                            
                        
                        if room:
                            break

                # Receiving total capacity
                return total

            # call the function for each row and add the result to a new column
            merged_df['Total Capacity'] = merged_df.apply(calculate_total_capacity, axis=1)

            x = merged_df['total_student'].values
            y = merged_df['Total Capacity'].values

            '''
            x = total student
            y = total capacity
            formula => d = |ax1 + by1 + c| / (a^2 + b^2)^0.5

            y = mx + b
            mx + b - y = 0
            m * total student - b + total capacity / (m^2 + 1)^0.5
            
            distance is 0 in terms of best case, we are finding max value via merged_df['distance'].max()

            dividing each distance value by the maximum distance turns the distances into ratios between 0 and 1 (merged_df['distance'] / merged_df['distance'].max()) Subtracting from 1 then transforms the scores into a score range where the highest score is 1 and the lowest score is 0. (1 - merged_df['distance'] / merged_df['distance'].max()) We did this because small distance should get the greater point
            '''
            m, b = np.polyfit(x, y, 1)

            # calculate the distance between line and dots. calculate the score
            merged_df['distance'] = abs(merged_df['total_student'] * m - merged_df['Total Capacity'] + b) / ((m**2 + 1)**0.5)
            merged_df['score'] = (1 - merged_df['distance'] / merged_df['distance'].max()) * 100

            total_score = merged_df['score'].sum()
            score_penalty = total_score / (len(merged_df) * merged_df['score'].max()) 

            print(score_penalty)
            print(merged_df)
            
            
            
            plt.scatter(x, y)

            # draw the line
            fit_fn = np.poly1d([m, b])
            plt.plot(x, fit_fn(x), '--k')

            # show the graph
            plt.show()

            # save the graph to the file
            plt.savefig('scatter_plot.png')


