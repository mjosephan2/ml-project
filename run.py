from part2.viterbi import viterbi
from preprocess import preprocess_train, preprocess_x_test
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--train_path", "-t", required=True)
parser.add_argument("--test_path", "-ts", required=True)
if __name__ == "__main__":
    train_path = "./data/CN/train"
    x_test_path = "./data/CN/dev.in"
    x_train, y_train = preprocess_train(train_path)
    x_test = preprocess_x_test(x_test_path)
    y_pred = viterbi(x_test, x_train, y_train)
    with open("dev.p2.out", "w", encoding="utf8") as f:
        out = []
        for x, y in zip(x_test, y_pred):
            temp_out = ""
            temp_out+="".join(x)
            temp_out+=" "
            temp_out+="".join(y)
            out.append(temp_out)
        f.write("\n".join(out))