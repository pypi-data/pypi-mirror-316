def ss_data():
    try:
        with open("project_Screenshot/dataset.txt", 'r') as file:
            for line in file:
                yield line.strip()
    except:
        return "Unable to connect the dataset"

if __name__ == '__main__':
    x = ss_data()
    print(next(x))
    print(next(x))

    