def read_samples(path):
    file = open(path, 'r')

    signal_type = bool(file.readline())
    is_periodic = bool(file.readline())
    samples_count = int(file.readline())

    x = []
    y = []

    for i in range(0, samples_count):
        line = file.readline().split()
        x.append(float(line[0]))
        y.append(float(line[1]))
    file.close()
    return x, y

