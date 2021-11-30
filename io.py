def read_data():
    with open('data.txt', 'r') as f:
        return list(line for line in f.readlines()):
