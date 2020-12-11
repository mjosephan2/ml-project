from collections import defaultdict
import pandas as pd

def emissions(x,y):
    count_x_given_y = defaultdict(int)
    count_y = defaultdict(int)
    for words, tags in zip(x,y):
        for w,t in zip(words, tags):
            count_x_given_y[(w,t)]+=1
            count_y[t]+=1
    emissions_y_to_x = {}
    #print(count_x_given_y)
    #print(count_y)
    for k,v in count_x_given_y.items():
        w,t = k
        emissions_y_to_x[(w,t)] = v / count_y[t]
    
    # turn into dataframe
    l = list(emissions_y_to_x.keys())
    cols = list(set([x[0] for x in l]))
    rows = list(set([x[1] for x in l]))
    number_cols = len(cols)
    number_rows = len(rows)
    dict_col_index = {c:i for i, c in enumerate(cols)}
    dict_row_index = {r:i for i, r in enumerate(rows)}
    values = [[0 for c in range(number_cols)] for r in range(number_rows)]
    #print(values)
    for k,v in emissions_y_to_x.items():
        w, t = k
        row_index = dict_row_index[t]
        col_index = dict_col_index[w]
        values[row_index][col_index] = v
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
    print(emissions(x,y))