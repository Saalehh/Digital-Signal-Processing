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

    signal = Signal(type=signal_type, is_periodic=is_periodic, x=x, y=y)
    return signal


class Signal:
    def __init__(self, type, is_periodic, x, y):
        self.type = type
        self.is_periodic = is_periodic
        self.x = x
        self.y = y

