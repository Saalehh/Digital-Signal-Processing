import numpy as np
import matplotlib.pyplot as plt


def plot_continuous_and_discrete(x, y, title="Graph Representation"):
    plt.style.use("fivethirtyeight")
    plt.plot(x, y, label='Continuous')
    plt.stem(x, y, linefmt='C1-', label='Discrete')  # linefmt specifies the color of the line, 'C1-' is a predefined color
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()


def plot_continuous(x, y, title="Contiuous Representation"):
    plt.style.use("fivethirtyeight")
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.grid(True)


def plot_discrete(x, y, title="Discrete Representation"):
    plt.style.use("fivethirtyeight")
    plt.stem(x, y, linefmt='C1-', markerfmt='C1o', basefmt=' ')
    plt.title(title)
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.grid(True)

