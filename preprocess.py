def preprocess_train(path):
    with open(path, "r", encoding="utf8") as f:
        data = f.readlines()
    x_data = []
    y_data = []
    x = []
    y = []
    for line in data:
        line = line.strip()
        if line==None or line=="":
            # end of the current sentence
            x_data.append(x)
            y_data.append(y)
            x = []
            y = []
            continue
        temp_x, temp_y = line.split()
        x.append(temp_x)
        y.append(temp_y)
    if x and y:
        x_data.append(x)
        y_data.append(y)
        x = []
        y = []
    return x_data ,y_data

def preprocess_x_test(path):
    with open(path, "r", encoding="utf8") as f:
        data = f.readlines()
    x_data = []
    x = []
    for line in data:
        line = line.strip()
        if line==None or line=="":
            # end of the current sentence
            x_data.append(x)
            x = []
            continue
        x.append(line)
    if x:
        x_data.append(x)
        x = []
    return x_data

if __name__ == "__main__":
    train_path = "./data/CN/train"
    test_path = "./data/CN/dev.in"
    x,y = preprocess_train(train_path)
    print(x[:10])
    print(y[:10]) 
    x_test = preprocess_x_test(test_path)
    print(x_test[:10])