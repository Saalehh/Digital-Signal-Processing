import math
import matplotlib.pyplot as plt
from tkinter import *
from functools import partial
from task1_test_cases.comparesignals import SignalSamplesAreEqual

# region Point 1

def plot_continuous_and_discrete(x, y):
    plt.style.use("fivethirtyeight")
    plt.plot(x, y, label='Continuous')
    plt.stem(x, y, linefmt='C1-', label='Discrete')  # linefmt specifies the color of the line, 'C1-' is a predefined color
    plt.title('Continuous and Discrete Representation')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()



def plot_continuous(x, y):
    plt.plot(x, y)
    plt.title('Continuous Representation')
    plt.xlabel('Time or Sample Index')
    plt.ylabel('Amplitude')
    plt.grid(True)

def plot_discrete(x, y):
    plt.stem(x, y, linefmt='C1-', markerfmt='C1o', basefmt=' ')
    plt.title('Discrete Representation')
    plt.xlabel('Time or Sample Index')
    plt.ylabel('Amplitude')
    plt.grid(True)


def read_samples(path):
    file = open(path, 'r')

    signal_type = bool(file.readline())
    is_periodic = bool(file.readline())
    samples_count = int(file.readline())

    x = []
    y = []

    for i in range(0, samples_count):
        line = file.readline().split()
        x.append(int(line[0]))
        y.append(float(line[1]))
    file.close()
    return x, y

x, y = read_samples('../signal1.txt')
# plot_continuous_and_discrete(x, y)
plt.figure(figsize=(12, 6))

# Create a 1x2 grid of subplots and plot in the first one
plt.subplot(1, 2, 1)
plot_continuous(x, y)

# Plot in the second subplot
plt.subplot(1, 2, 2)
plot_discrete(x, y)

plt.tight_layout()  # Ensures that the plots don't overlap
plt.show()


# endregion

# region Point 2

def generate_signal_plot(A, Fa, Fs, phi, type):
    A = int(A.get())
    Fa = int(Fa.get())
    Fs = int(Fs.get())
    phi = float(phi.get())
    type = type.get()

    gen_x = []  # INDICES
    gen_y = []  # SAMPLES
    for i in range(0, Fs):
        gen_x.append(i)
        if type == 'sin':
            gen_y.append(A * math.sin(2 * math.pi * Fa * (i / Fs) + phi))
        else:
            gen_y.append(A * math.cos(2 * math.pi * Fa * (i / Fs) + phi))
    # TESTING #
    if type == 'sin':
        SignalSamplesAreEqual('SinOutput.txt', gen_x, gen_y)
    else:
        SignalSamplesAreEqual('CosOutput.txt', gen_x, gen_y)
    # DRAWING SIGNALS #
    # Create a 1x2 grid of subplots and plot in the first one
    plt.subplot(1, 2, 1)
    plot_continuous(gen_x, gen_y)

    # Plot in the second subplot
    plt.subplot(1, 2, 2)
    plot_discrete(gen_x, gen_y)

    plt.tight_layout()  # Ensures that the plots don't overlap
    plt.show()


# region   TKINTER
win = Tk()
win.geometry("500x400")
A = StringVar()
Fa = StringVar()
Fs = StringVar()
phi = StringVar()
sigType = StringVar()
# endregion
# region WIDGETS
amp_label = Label(win, text='Amplitude:')
amp_label.place(x=130, y=50)
amp_entry = Entry(win, textvariable=A)
amp_entry.place(x=250, y=50)

phi_label = Label(win, text='Phase Shift:')
phi_label.place(x=130, y=100)
phi_entry = Entry(win, textvariable=phi)
phi_entry.place(x=250, y=100)

Fa_label = Label(win, text='Analog Frequency:')
Fa_label.place(x=130, y=150)
Fa_entry = Entry(win, textvariable=Fa)
Fa_entry.place(x=250, y=150)

Fs_label = Label(win, text='Sampling Frequency:')
Fs_label.place(x=130, y=200)
Fs_entry = Entry(win, textvariable=Fs)
Fs_entry.place(x=250, y=200)

sigType_label = Label(win, text='Signal Generation:')
sigType_label.place(x=130, y=250)
options = ['sin', 'cos']
sigType.set('sin')
dropMenu = OptionMenu(win, sigType, *options)
dropMenu.place(x=250, y=245)

button = Button(win, text='Generate', command=partial(generate_signal_plot, A, Fa, Fs, phi, sigType), activeforeground='red')
button.place(x=230, y=350)

win.mainloop()
# endregion

# endregion
