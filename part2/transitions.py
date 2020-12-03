from collections import defaultdict
import numpy as np
import pandas as pd

def transitions(y):
    num_data = len(y)
    count_y = defaultdict(int)
    count_u_to_v = defaultdict(int)
    START = "START"
    STOP = "STOP"
    count_y[START]=num_data
    count_y[STOP]=num_data
    for tags in y:
        tags = [START] + tags + [STOP]
        prev = START
        for curr in tags[1:]:
            count_u_to_v[(prev,curr)]+=1
            if curr!=STOP:
                count_y[curr]+=1
            prev = curr
    transitions_u_v = defaultdict(int)
    for (u,v), count in count_u_to_v.items():
        transitions_u_v[(u,v)] = count / count_y[u]
    
    # turn into dataframe
    unique_tags = [START] + list(set([item for sublist in y for item in sublist])) + [STOP]
    cols = unique_tags[1:]
    rows = unique_tags[:-1]
    number_cols = len(cols)
    number_rows = len(rows)
    dict_col_index = {c:i for i, c in enumerate(cols)}
    dict_row_index = {r:i for i, r in enumerate(rows)}
    values = [[0 for c in range(number_cols)] for r in range(number_rows)]
    #print(values)
    for key,val in transitions_u_v.items():
        u, v = key
        row_index = dict_row_index[u]
        col_index = dict_col_index[v]
        values[row_index][col_index] = val
    df = pd.DataFrame(data=values,columns=cols, index=rows)
    return df

if __name__ == "__main__":
    x = [["b", "c", "a", "b"],
        ["a","b","a"],
        ["b","c","a","b","d"],
        ["c","b","a"],
        ["d"],
        ["d","b"]]
    y = [["X","X","Z","X"],
        ["X","Z","Y"],
        ["Z","Y","X","Z","Y"],
        ["Z","Z","Y"],
        ["Z"],
        ["X","Z"]]
    print(transitions(y))