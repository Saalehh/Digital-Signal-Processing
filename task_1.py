import math
import tkinter as tk
from tkinter import ttk
from functools import partial
from plotting import *


def get_discrete_signal_dimensions(amplitude, analog_freq, sampling_freq, phase_shift, signal_type):
    amplitude = int(amplitude.get())
    analog_freq = int(analog_freq.get())
    sampling_freq = int(sampling_freq.get())
    phase_shift = float(phase_shift.get())
    signal_type = signal_type.get()

    indexes = []
    values = []
    if signal_type == 'sin':
        for i in range(0, sampling_freq):
            indexes.append(i)
            values.append(amplitude * math.sin((2 * math.pi * analog_freq * (i / sampling_freq)) + phase_shift))
    elif signal_type == 'cos':
        for i in range(0, sampling_freq):
            indexes.append(i)
            values.append(amplitude * math.cos((2 * math.pi * analog_freq * (i / sampling_freq)) + phase_shift))

    return indexes, values


def generate_signals_plot(amplitude, analog_freq, sampling_freq, phase_shift, signal_type):
    discrete_x, discrete_y = get_discrete_signal_dimensions(amplitude, analog_freq, sampling_freq, phase_shift,
                                                            signal_type)
    # DRAWING SIGNALS #
    # Create a 1x2 grid of subplots and plot in the first one
    plt.subplot(1, 2, 1)
    plot_continuous( discrete_x, discrete_y)

    # Plot in the second subplot
    plt.subplot(1, 2, 2)
    plot_discrete(discrete_x, discrete_y)

    plt.tight_layout()  # Ensures that the plots don't overlap
    plt.show()


# region GUI
win = tk.Tk()
win.geometry("500x500")
win.configure(bg="black")
win.title("Draw Signal")

amplitude = tk.StringVar()
analog_freq = tk.StringVar()
sampling_freq = tk.StringVar()
phase_shift = tk.StringVar()
signal_type = tk.StringVar()

# Create a style object for ttk widgets
style = ttk.Style()

inputs_frame = tk.Frame(win)
inputs_frame.columnconfigure(0, weight=1)
inputs_frame.columnconfigure(1, weight=1)
inputs_frame.columnconfigure(2, weight=1)
inputs_frame.configure(bg="black")

# Labels
style.configure("TLabel", foreground="white", background="black", font=("Arial", 14, "bold"))
amp_label = ttk.Label(inputs_frame, text='Amplitude:')
amp_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

phi_label = ttk.Label(inputs_frame, text='Phase Shift:')
phi_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

Fa_label = ttk.Label(inputs_frame, text='Analog Frequency:')
Fa_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

Fs_label = ttk.Label(inputs_frame, text='Sampling Frequency:')
Fs_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')

sigType_label = ttk.Label(inputs_frame, text='Signal Type:')
sigType_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')

# Entry Widgets
style.configure("TEntry", font=("Arial", 12, "bold"))
amp_entry = ttk.Entry(inputs_frame, textvariable=amplitude)
amp_entry.grid(row=0, column=1, padx=10, pady=10)

phi_entry = ttk.Entry(inputs_frame, textvariable=phase_shift)
phi_entry.grid(row=1, column=1, padx=10, pady=10)

Fa_entry = ttk.Entry(inputs_frame, textvariable=analog_freq)
Fa_entry.grid(row=2, column=1, padx=10, pady=10)

Fs_entry = ttk.Entry(inputs_frame, textvariable=sampling_freq)
Fs_entry.grid(row=3, column=1, padx=10, pady=10)

# OptionMenu (Combobox)
style.configure("TCombobox", font=("Arial", 12, "bold"))
options = ['sin', 'cos']
signal_type.set('sin')

drop_menu = ttk.Combobox(inputs_frame, textvariable=signal_type, values=options)
drop_menu.grid(row=4, column=1, padx=10, pady=10)
inputs_frame.pack(pady=50)

# Generate Button
style.configure("TButton", foreground="black", background="black", font=("Arial", 14, "bold"))
button = ttk.Button(win, text='Generate',
                    command=partial(generate_signals_plot, amplitude, analog_freq, sampling_freq, phase_shift,
                                    signal_type))
button.pack(side="bottom", pady=30)

win.mainloop()
# endregion
