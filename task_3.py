import math
import tkinter as tk
from tkinter import ttk
from functools import partial
from helper_functions import *
from plotting import *
from QuanTest1 import QuantizationTest1
from QuanTest2 import QuantizationTest2


def generate_signal_plot(in_type, l, b, tst):
    in_type = input_type.get()
    tst = test.get()

    if in_type == '2':
        b = int(bits.get())
        l = int(math.pow(2, b))
    else:
        l = int(levels.get())
        b = int(math.log(l, 2))

    if tst == '1':
        x, y = read_samples('task3_test1/Quan1_input.txt')
    else:
        x, y = read_samples('task3_test2/Quan2_input.txt')

    # Find min & max
    mini = min(y)
    maxi = max(y)

    # Find delta
    delta = (maxi - mini) / l

    # Ranges & Midpoints
    ranges = []
    midpoints = []
    last = mini
    for i in range(l):
        if i > 0:
            last = ranges[i - 1][1]
        ranges.append([last, round(last + delta, 4)])
        midpoints.append(round((last + last + delta) / 2, 4))

    # Intervals
    interval_index = []
    for i in range(len(x)):
        for j in range(len(ranges)):
            if ranges[j][0] <= y[i] <= ranges[j][1]:
                interval_index.append(j + 1)
                break

    # Quantization
    quantized_values = []
    error = []
    avg_error = 0
    for i in range(len(interval_index)):
        quantized_values.append(midpoints[interval_index[i] - 1])
        error.append(round(midpoints[interval_index[i] - 1] - y[i], 4))
        avg_error += (error[-1] * error[-1])
    avg_error = avg_error / len(x)
    print('Quantized values:', quantized_values)
    print('Quantization Error:', error)
    print('Average Power Error:', avg_error)
    plot_continuous_and_discrete(x, quantized_values)

    # Encoding
    encoded_values = []
    for i in interval_index:
        encoded_values.append(bin(i - 1)[2:].zfill(b))  # Remove 0b prefix and put leading zeros
    print('Encoded Signal', encoded_values)
    plot_continuous_and_discrete(x, interval_index)

    if tst == '1':
        QuantizationTest1('task3_test1/Quan1_Out.txt', encoded_values, quantized_values)
    else:
        QuantizationTest2('task3_test2/Quan2_Out.txt', interval_index, encoded_values,
                          quantized_values, error)


def toggle_levels_visibility_on():
    levels_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
    bits_entry.grid_forget()


def toggle_bits_visibility_on():
    bits_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
    levels_entry.grid_forget()


# region GUI

win = tk.Tk()
win.geometry("500x500")
win.title("Signal Generator")
win.configure(bg="black")

input_type = tk.StringVar()
levels = tk.StringVar()
bits = tk.StringVar()
test = tk.StringVar()

style = ttk.Style()
style.configure("TLabel", foreground="white", background="black", font=("Arial", 14, "bold"))
style.configure("TEntry", font=("Arial", 12, "bold"))
style.configure("TRadiobutton", foreground="white", background="black", font=("Arial", 14, "bold"))
style.configure("TButton", foreground="black", background="black", font=("Arial", 14, "bold"))

radio_frame = tk.Frame(win)
radio_frame.configure(bg="black")

levels_radio = ttk.Radiobutton(radio_frame, text='Levels Number:', variable=input_type, value="Levels",
                               style="TRadiobutton", command=toggle_levels_visibility_on)
levels_radio.grid(row=0, column=0, padx=10, pady=10, sticky='w')
levels_entry = ttk.Entry(radio_frame, textvariable=levels, style="TEntry")

bits_radio = ttk.Radiobutton(radio_frame, text='Bits Number:', variable=input_type, value="Bits", style="TRadiobutton",
                             command=toggle_bits_visibility_on)
bits_radio.grid(row=1, column=0, padx=10, pady=10, sticky='w')
bits_entry = ttk.Entry(radio_frame, textvariable=bits, style="TEntry")

test_label = ttk.Label(radio_frame, text='Test Number:', style="TLabel")
test_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')
test_entry = ttk.Entry(radio_frame, textvariable=test, style="TEntry")
test_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

radio_frame.pack(pady=50)

button = ttk.Button(win, text='Generate', command=partial(generate_signal_plot, input_type, levels, bits, test),
                    style="TButton")
button.pack(side="bottom", pady=30)
win.mainloop()

# endregion
