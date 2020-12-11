from collections import defaultdict
from .emissions_with_unk import emissions
from .transitions import transitions


def viterbi_top_k(x_test, x_train, y_train, top_k):
    emissions_df = emissions(x_train,y_train)
    transitions_df = transitions(y_train)
    tags = emissions_df.index.values

    #print(transitions_df)
    y_preds = []
    
    print("Start predictions")
    count = 1
    for words in x_test:
        print(f"Prediction {count}")
        dp = forward(words, tags, emissions_df, transitions_df, top_k)
        # print(dp)
        result = backtracking(dp, words, tags, emissions_df, transitions_df,  top_k)
        # print(result)
        y_preds.append(result[-1])
        count+=1
    print("Done")
    return y_preds

def backtracking(dp, words, tags, emissions_df, transitions_df, top_k):
    START = "START"
    STOP = "STOP"
    UNK = "UNK"
    n = len(words)
    padded_words = [START] + words + [STOP]
    results = []

    # From STOP to n
    for u in tags:
        for score in dp[(n, u)]:
            results.append((score, [u], score * transitions_df.at[u, STOP]))
    results = sorted(results, reverse=True, key=lambda x: x[2])
    results = results[:top_k]

    # From n to START (exclusive START)
    for j in range(n-1, 0, -1):
        # help with gettings the latest tag
        placeholder_argmax = [r_tags for (score_j, r_tags, _) in results]
        temp_results = []

        # loop over all possible tags
        for u in tags:
            # loop over the top 3 score at j
            for score in dp[(j, u)]:
                # loop over the top 3 tags sequence at j+1
                for r_tags in placeholder_argmax:
                    t = r_tags[-1]
                    try:
                        b_u_o = emissions_df.at[t,padded_words[j+1]]
                    except KeyError:
                        b_u_o = emissions_df.at[u,UNK]
                    score_j_1 = score * transitions_df.at[u, t] * b_u_o
                    temp_results.append((score, r_tags + [u], score_j_1))
        new_results = []
        # not sorting but finding closest
        for (score_j, t, score_j_1) in results:
            new_score_j, t, new_score_j_1 = min(temp_results, key=lambda x: abs(x[2]-score_j))
            new_results.append((new_score_j,t, new_score_j_1))
        results = new_results
    output = []
    for i in range(len(results)):
        output.append(list(reversed(results[i][1])))
    return output

def forward(words, tags, emissions_df, transitions_df, top_k):
    START = "START"
    STOP = "STOP"
    UNK = "UNK"
    dp = {}
    # dp [(j, tag, top_k_position)]
    dp[(0, START)] = 1
    # ensuring that the range is from 0 to n+1
    n = len(words)
    padded_words = [START] + words + [STOP]

    # top_k means k [0,top_k)
    # START loop
    for u in tags:
        try:
            b_u_o = emissions_df.at[u,padded_words[1]]
        except KeyError:
            b_u_o = emissions_df.at[u,UNK]
        dp[(1, u)]= [dp[(0,START)] * b_u_o *  transitions_df.at[START,u]]

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
                for score in dp[(j,v)]:
                    sequences.append(score * b_u_o *  transitions_df.at[v,u])
            sequences = sorted(sequences, reverse=True)
            dp[(j+1, u)]= sequences[:top_k]
    # Stop
    sequences = []
    for v in tags:
        for score in dp[(n,v)]:
            sequences.append(score * transitions_df.at[v,STOP])
    sequences = sorted(sequences, reverse=True)
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
