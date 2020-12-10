from .emissions_with_unk import emissions
def simple_sentiment(x_test, x_train, y_train):
    # placeholder for results
    ypreds = []
    # x_test is array of list of word
    emissions_df = emissions(x_train, y_train)
    for words in x_test:
        y = []
        for w in words:
            # check if the word exits in the training set, otherwise set the word to UNK
            training_words = emissions_df.columns
            if w not in training_words:
                w = 'UNK'
            # get tag with maximum emission probability
            t = emissions_df.loc[:,w].idxmax()
            y.append(t)
        ypreds.append(y)
    return ypreds

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
    print(simple_sentiment([["a","d"]], x, y))