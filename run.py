from part2.simple_sentiment import simple_sentiment
from part3.viterbi import viterbi
from preprocess import preprocess_train, preprocess_x_test
from os.path import join
import argparse

models = ["viterbi", "simple_sentiment"]
parser = argparse.ArgumentParser()
parser.add_argument("--model","-m", required=True, help="viterbi | simple_sentiment")
parser.add_argument("--predict_dir", "-p", required=True, help="input directory that contains training data (train) and test input (dev.in)")
args = parser.parse_args()

if __name__ == "__main__":
    model = args.model
    if model not in models:
        raise Exception("Please input the correct model name! "+" or ".join(models))
    dir = args.predict_dir
    train_path = join(dir, "train")
    x_test_path = join(dir, "dev.in")
    x_train, y_train = preprocess_train(train_path)
    x_test = preprocess_x_test(x_test_path)

    y_preds = []
    fileName = ""
    if model=="viterbi":
        y_preds = viterbi(x_test, x_train, y_train)
        fileName = "dev.p3.out"
    elif model=="simple_sentiment":
        y_preds = simple_sentiment(x_test, x_train, y_train)
        fileName = "dev.p2.out"

    with open(join(dir,fileName), "w", encoding="utf8") as f:
        out = []
        for x_list, y_list in zip(x_test, y_preds):
            temp_out = []
            # x and y are list of words and tags
            for w,t in zip(x_list, y_list):
                line = w+" "+t
                temp_out.append(line)
            out.append("\n".join(temp_out)+"\n")
        f.write("\n".join(out))

    # with open(join(dir,fileName), "w", encoding="utf8") as f:
    #     out = []
    #     for x, y in zip(x_test, y_preds):
    #         temp_out = ""
    #         temp_out+="".join(x)
    #         temp_out+=" "
    #         temp_out+="".join(y)
    #         out.append(temp_out)
    #     f.write("\n".join(out))