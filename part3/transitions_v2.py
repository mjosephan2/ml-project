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
    
    #transitions_u_v is a dict of form {(u,v): transition_probability}
    # turn into dataframe
    unique_tags = [START] + list(set([item for sublist in y for item in sublist])) + [STOP]
    cols = unique_tags[1:]
    rows = unique_tags[:-1]
    df = pd.DataFrame(columns=cols, index=rows)
    for key, val in transitions_u_v.items():
        u, v = key
        df.at[u,v] = val
    
    df = df.fillna(0)
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