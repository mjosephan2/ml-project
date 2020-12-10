from collections import defaultdict
from emissions_with_unk import emissions
from transitions import transitions


def viterbi(x_test, x_train, y_train):
    emissions_df = emissions(x_train,y_train)
    transitions_df = transitions(y_train)
    tags = emissions_df.index.values

    #print(transitions_df)
    y_preds = []
    number_of_data = len(x_test)
    
    print("Start predictions")
    count = 1
    for words in x_test:
        print(f"Prediction {count}")
        dp = forward(words, tags, emissions_df, transitions_df)
        result = backtracking(dp, words, tags, transitions_df)
        y_preds.append(result)
        count+=1
    print("Done")
    return y_preds

def backtracking(dp, words, tags, transitions_df):
    START = "START"
    STOP = "STOP"
    n = len(words)
    results = []
    argmax = None
    maximum = 0

    # From STOP to n
    for u in tags:
        score = dp[(n, u)] * transitions_df.loc[u, STOP]
        if score >= maximum:
            maximum = score
            argmax = u
    results.append(argmax)

    # From n to START (exclusive START)
    # utilizes the argmax found before
    for j in range(n-1, 0, -1):
        maximum = 0
        placeholder_argmax = argmax
        for u in tags:
            score = dp[(j, u)] * transitions_df.loc[u, placeholder_argmax]
            if score >= maximum:
                maximum = score
                argmax = u
        results.append(argmax)
        # set the new placeholder
        placeholder_argmax = argmax
    return results[::-1]

def forward(words, tags, emissions_df, transitions_df):
    START = "START"
    STOP = "STOP"
    UNK = "UNK"
    dp = {}
    dp[(0, START)] = 1
    # ensuring that the range is from 0 to n+1
    n = len(words)
    padded_words = [START] + words + [STOP]
    # 0 to n-1
    for j in range(n):
        # loop through all tags excluding STOP
        if j==0:
            v_list = [START]
        else:
            v_list = tags
        for u in tags:
            try:
                b_u_o = emissions_df.loc[u,padded_words[j+1]]
            except KeyError:
                b_u_o = emissions_df.loc[u,UNK]
            dp[(j+1, u)]=max([
                dp[(j,v)] * b_u_o *  transitions_df.loc[v,u] for v in v_list
                ])
    # Stop 
    dp[(n+1, STOP)] = max([
        dp[(n,v)] * transitions_df.loc[v,STOP] for v in tags
    ])
    return dp

if __name__ == "__main__":
    x = [
        ["b", "c", "a", "b"],
        ["a","b","a"],
        ["b","c","a","b","d"],
        ["c","b","a"],
        ["d"],
        ["d","b"]
    ]
    y = [
        ["X","X","Z","X"],
        ["X","Z","Y"],
        ["Z","Y","X","Z","Y"],
        ["Z","Z","Y"],
        ["Z"],
        ["X","Z"]
    ]
    print(viterbi([["a","d"], ["b"]], x, y))
