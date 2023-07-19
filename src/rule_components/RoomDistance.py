from rule_components.Rule import Rule
import pandas as pd
import numpy as np



class RoomDistance(Rule):
    def __init__(self,data_obj):
        super().__init__(data_obj)
        self.score, self.plot_arr,self.conflicts_df = self.compute()
    def compute(self):
        df = pd.concat([self.data_obj.exam_form,self.data_obj.exam_rooms],axis=1)
        df = df[(df['Form'] != 'muendlich') & (df['Form'] != 'online')]

        def create_sub_matrix(desired_rooms):
            return self.data_obj.room_distances.loc[desired_rooms,desired_rooms]
        def calculate_sub_score(sub_matrix):
            # find the maximum distance in the entire distance matrix
            max_distance = self.data_obj.room_distances.max().max()
            min_distance = 5
            # only takes the left triangle and converts to an array
            triangle = np.triu(sub_matrix).flatten() 
            # remove the zero values
            sub_distances = [num for num in triangle if int(num)!=0] 
            avg_distance = np.sum(sub_distances) / len(sub_distances)
            # we need to normalize these averages
            score = (1-((avg_distance - min_distance) / (max_distance - min_distance)))*100
            return score
            
        def calculate_score():
            scores=[]
            for rooms in df['HS']:
                if(len(rooms)>1):
                    sub_matrix = create_sub_matrix(rooms)
                    scores.append(calculate_sub_score(sub_matrix))
                    total_score = sum(scores)/len(scores)
            return total_score
            
        percantage_score = calculate_score()
        return percantage_score, None, None