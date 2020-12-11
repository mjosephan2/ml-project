from collections import defaultdict
from emissions_with_unk import emissions
from transitions import transitions


def viterbi_top_k(x_test, x_train, y_train, top_k):
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
        dp = forward(words, tags, emissions_df, transitions_df, top_k)
        # print(dp)
        result = backtracking(dp, words, tags, transitions_df, top_k)
        # print(result)

        # append kth best
        print(result)
        y_preds.append(result[-1])
        count+=1
    print("Done")
    return y_preds

def backtracking(dp, words, tags, transitions_df, top_k):
    START = "START"
    STOP = "STOP"
    n = len(words)
    results = []

    # From STOP to n
    trackings = dp[(n+1, STOP)]

    # set results
    for score, prev_tag, seq in trackings:
        results.append([prev_tag])
    # From n to START (exclusive START)
    for j in range(n, 1, -1):
        new_trackings = []
        for score, prev_tag, seq in trackings:
            new_trackings.append(dp[(j, prev_tag)][seq])
        
        # update results
        for i in range(len(new_trackings)):
            score, prev_tag, seq = new_trackings[i]
            results[i].append(prev_tag)
    # reverse order
    for i in range(len(results)):
        results[i].reverse()
    return results

def forward(words, tags, emissions_df, transitions_df, top_k):
    START = "START"
    STOP = "STOP"
    UNK = "UNK"
    dp = {}
    # dp [(j, tag)] = (score, prev_tag, seq)
    # seq => [0, top_k)
    dp[(0, START)] = (1, None, None)
    # ensuring that the range is from 0 to n+1
    n = len(words)
    padded_words = [START] + words + [STOP]

    # START loop
    for u in tags:
        try:
            b_u_o = emissions_df.at[u,padded_words[1]]
        except KeyError:
            b_u_o = emissions_df.at[u,UNK]
        dp[(1, u)]= [
            (dp[(0,START)][0] * b_u_o *  transitions_df.at[START,u] , START, 0)
            ]

    # 0 to n-1
    for j in range(1,n):
        # loop through all tags excluding STOP
        v_list = tags
        for u in tags:
            try:
                b_u_o = emissions_df.at[u,padded_words[j+1]]
            except KeyError:
                b_u_o = emissions_df.at[u,UNK]
            sequences = []
            for v in v_list:
                for i, (score, prev_tag, seq) in enumerate(dp[(j,v)]):
                    # new_score, current tag, current sequence
                    sequences.append((score * b_u_o *  transitions_df.at[v,u], v, i))
            sequences = sorted(sequences, reverse=True, key=lambda x: x[0])
            top_k_sequences = sequences[:top_k]
            dp[(j+1, u)]= top_k_sequences
    # Stop
    sequences = []
    for v in tags:
        for i, (score, prev_tag, seq) in enumerate(dp[(n,v)]):
            sequences.append((score * transitions_df.at[v,STOP], v, i))
    sequences = sorted(sequences, reverse=True, key=lambda x: x[0])
    dp[(n+1, STOP)] = sequences[:top_k]
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
    print(viterbi_top_k([["a","d","b","c"]], x, y, 3)) # X,X,Z,Y
    print(viterbi_top_k([["a","d"]], x, y, 3)) # Z,Y
