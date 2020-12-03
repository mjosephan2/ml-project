def preprocess_train(path):
    with open(path, "r", encoding="utf8") as f:
        data = f.read().split('\n')
    x = []
    y = []
    for line in data:
        line = line.strip()
        if line==None or line=="":
            continue
        temp_x, temp_y = line.split()
        x.append([temp_x])
        y.append([temp_y])
    return x,y

def preprocess_x_test(path):
    with open(path, "r", encoding="utf8") as f:
        data = f.read().split('\n')
    x = []
    for line in data:
        line = line.strip()
        if line==None or line=="":
            continue
        x.append([line])
    return x

if __name__ == "__main__":
    train_path = "./data/CN/train"
    test_path = "./data/CN/dev.in"
    x,y = preprocess_train(train_path)
    print(x[:10])
    print(y[:10]) 
    x_test = preprocess_x_test(test_path)
    print(x_test[:10])