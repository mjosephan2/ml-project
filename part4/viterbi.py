from collections import defaultdict
from emissions_with_unk import emissions
from transitions import transitions


def viterbi(x_test, x_train, y_train, top_k):
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
        print(dp)
        result = backtracking(dp, words, tags, transitions_df, top_k)
        print(result)
        # y_preds.append(result)
        count+=1
    print("Done")
    return y_preds

def backtracking(dp, words, tags, transitions_df, top_k):
    START = "START"
    STOP = "STOP"
    n = len(words)
    results = []

    # From STOP to n
    # results = [(score at j, seq, score at j+1)]
    for u in tags:
        for score in dp[(n, u)]:
            results.append((score, [u], score * transitions_df.at[u, STOP]))
    # score at j+1 only useful at this sorting part
    results = sorted(results, reverse=True, key=lambda x: x[2])
    results = results[:top_k]

    # From n to START (exclusive START)
    # placeholder for convenient value comparisons
    placeholder_results = [(score_j, tags, score_j_1) for (score_j, tags, score_j_1) in results]
    for j in range(n-1, 0, -1):
        placeholder_argmax = [tags for (score_j, tags, _) in results]
        temp_results = []

        for u in tags:
            for score in dp[(j, u)]:
                for tags in placeholder_argmax:
                    t = tags[-1]
                    score_j_1 = score * transitions_df.at[u, t]
                    temp_results.append((score, tags + [u], score_j_1))
        new_results = []
        # not sorting but finding closest
        print(temp_results)
        for (score_j, tags, score_j_1) in results:
            print(score_j)
            new_score_j, t, new_score_j_1 = min(temp_results, key=lambda x: abs(x[2]-score_j))
            print(new_score_j_1)
            new_results.append((new_score_j,t, new_score_j_1))
        results = new_results
    print(placeholder_results)
    return results

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
    print(viterbi([["a","d","b","c"]], x, y, 3)) # X,X,Z,Y
    print(viterbi([["a","d"]], x, y, 3)) # Z,Y
