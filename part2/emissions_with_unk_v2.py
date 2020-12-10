from collections import defaultdict
import pandas as pd

def emissions(x,y, k=0.5):
    UNK = "UNK"
    count_x_given_y = defaultdict(int)
    count_y = defaultdict(int)
    for words, tags in zip(x,y):
        for w,t in zip(words, tags):
            count_x_given_y[(w,t)]+=1
            count_y[t]+=1
    emissions_y_to_x = {}
    #print(count_x_given_y)
    #print(count_y)
    for key,val in count_x_given_y.items():
        w,t = key
        emissions_y_to_x[(w,t)] = val / (count_y[t]+k)
    
    # adding unknown
    for t, t_count in count_y.items():
        emissions_y_to_x[(UNK,t)] = k/(t_count+k)

    #emissions_y_to_x is a dict of form {(word, tag): count}
    # turn into dataframe
    l = list(emissions_y_to_x.keys())
    cols = list(set([x[0] for x in l])) #list of words without duplicates
    rows = list(set([x[1] for x in l])) #list of tags without duplicates
    
    df = pd.DataFrame(index= rows, columns= cols)
    for key,val in emissions_y_to_x.items():
        w, t = key
        df.at[t, w] = val
    
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
    df = emissions(x,y)
    print(df)