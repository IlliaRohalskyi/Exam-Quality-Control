import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_excel('input_data_files/FIW_Exams_2022ws.xlsx')

# Exclude the exams which will be held in the form of online or oral
df = df[~df['Form'].isin(['muendlich', 'online'])]
room_df = df[['Lehrveranstaltung', 'HS']]

# Split the exam room names into a list for each row
room_df['HS'] = room_df['HS'].apply(lambda x: x.split(','))

# Distance Matrix
def read_room_distances():
    distance_matrix = pd.read_excel('input_data_files/room_distance_matrix.xlsx')
    distance_matrix.index=distance_matrix.columns
    # print(distance_matrix)
    return distance_matrix

distance_matrix = read_room_distances()
max_distance = distance_matrix.max().max()  # find the maximum distance in the entire distance matrix
min_distance = 5

# Random distance generator
def create_random_distance_matrix(rooms):
    n = len(rooms)
    # create a random distance matrix of size n x n
    distance_matrix = pd.DataFrame(np.random.randint(1, 100, size=(n, n)), rooms, rooms)

    # set the diagonal elements to zero since the distance between a node and itself is zero
    np.fill_diagonal(distance_matrix.values, 0)

    # make the matrix symmetric
    distance_matrix = distance_matrix.where(np.triu(np.ones(distance_matrix.shape)).astype(bool))
    distance_matrix = distance_matrix.fillna(distance_matrix.T)

    #print(distance_matrix)
    return distance_matrix


def create_sub_matrix(distance_matrix, desired_rooms):
    sub_matrix = distance_matrix.loc[desired_rooms, desired_rooms]
    print(sub_matrix)

    return sub_matrix



def show_distance_graph(distance_matrix,sub_matrix):

    G = nx.from_pandas_adjacency(distance_matrix)
    subgraph = nx.from_pandas_adjacency(sub_matrix)

    pos = nx.spring_layout(G)
    # Draw the graph
    nx.draw_networkx(G, pos=pos, with_labels=True, node_color='lightblue', node_size=200, font_size=12)

    # Set the edge color for the desired edges
    edge_colors = ['black' if edge in subgraph.edges() else 'lightgrey' for edge in G.edges()]

    # Draw the edges with the desired colors
    nx.draw_networkx_edges(G, pos=pos, edge_color=edge_colors)

    # Draw the edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # Show the plot
    plt.show()


# Create a dictionary which will store the exam names as a key and the exam room/s for each exam as a value of matrix
def create_room_dic():
    total_score = 0
    room_distances = {}
    for index, row in room_df.iterrows():
        if len(row['HS']) > 1:  # check if the exam has more than one room -we'll check only them
            desired_rooms = [room.strip() for room in row['HS']]
            sub_matrix = create_sub_matrix(distance_matrix, desired_rooms)
            score = calculate_score(sub_matrix, room_distances)
            print(row['Lehrveranstaltung'])
            print(sub_matrix)
            print()
            print(score)
            total_score += score

            sub_dic = {
                'sub-matrix': sub_matrix,
                'score': score
            }
            room_distances[row['Lehrveranstaltung']] = sub_dic

            # show_distance_graph(sub_matrix)

    total_score = (total_score/(len(room_distances)*100))*100
    print(f'TOTAL SCORE IS: {total_score}')
    dene = pd.DataFrame.from_dict(room_distances)
    # print(dene)
    return room_distances

    # for i in room_distances:
    #     print(i)
    #     print(room_distances[i])

def calculate_score(sub_matrix, room_distances):

    triangle = np.triu(sub_matrix).flatten() # only takes the left triangle and converts to an array
    sub_distances = [num for num in triangle if int(num)!=0] # remove the zero values
    avg_distance = np.sum(sub_distances) / len(sub_distances)

    # we need to normalize these averages
    score = (1-((avg_distance - min_distance) / (max_distance - min_distance)))*100
    return score

room_distances = create_room_dic()

# for i in room_distances:
#     print(i,room_distances[i])

print(distance_matrix)
demo_sub_matrix=create_sub_matrix(distance_matrix,["H.1.1", "H.1.2", "H.1.3","H.1.11"])
# print(demo_sub_matrix)
show_distance_graph(distance_matrix,demo_sub_matrix)