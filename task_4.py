import math
import tkinter
import matplotlib.pyplot as plt
from plotting import *
from helper_functions import *
import cmath
import os
from tkinter import *
from functools import partial
from task4_signalcompare import *
from task1_comparesignals import *


def dft(signal):
    index, x = read_samples(signal)
    N = len(x)
    x_k = []

    for k in range(N):
        summation = 0
        for n in range(N):
            exp_term = cmath.exp(-1j * (2 * cmath.pi * n * k / N))
            term = x[n] * exp_term
            summation += term
        real_part = summation.real
        imag_part = summation.imag
        x_k.append(complex(real_part, imag_part))
    return x_k


def get_amp_phase(dft_set):
    amps = []
    phases = []
    for n in range(len(dft_set)):
        amps.append(round(math.sqrt((dft_set[n].real * dft_set[n].real) + (dft_set[n].imag * dft_set[n].imag)), 13))
        # phases.append(math.degrees(math.atan(dft_set[n].imag / dft_set[n].real)))
    phases = np.angle(dft_set)
    return amps, phases


def creat_signal_file(amps, phases):
    # Specify the directory and file name
    directory = "task_4_saved_signals"
    file_name = "created_signal.txt"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create the file within the directory and open it in write mode
    file_path = os.path.join(directory, file_name)
    radians = [math.radians(phase) for phase in phases]
    N = len(amps)
    try:
        with open(file_path, "w") as file:
            file.write("0\n")
            file.write("1\n")
            file.write(f"{N}\n")
            for i in range(N):
                file.write(f"{amps[i]} {radians[i]}\n")
    except FileNotFoundError:
        print("File not found!")


def sketch_dft(amps, phases, Fs):
    # Sketching the frequency versus amplitude
    N = len(amps)
    omega = (2 * cmath.pi * Fs) / N
    x = [i * omega for i in range(1, N+1)]

    plt.subplot(1, 2, 1)
    plot_discrete(x, amps, title='Frequency vs Amplitude')
    # Sketching the frequency versus phase
    plt.subplot(1, 2, 2)
    plot_discrete(x, phases, title='Frequency vs Phase')
    plt.tight_layout()
    plt.show()


def calculate_x_k(amps, phases):
    x_k = []
    for amp, phase in zip(amps, phases):
        real_part = amp * math.cos(phase)
        imaginary_part = amp * math.sin(phase)
        x_k.append(complex(real_part, imaginary_part))
    return x_k


def idft(amps_phases):
    amps, phases = read_samples(amps_phases)

    N = len(phases)
    indexes = []
    x_n = []
    x = calculate_x_k(amps, phases)

    for n in range(N):
        summation = 0
        indexes.append(n)
        for k in range(N):
            exp_term = cmath.exp(1j * (2 * cmath.pi * n * k / N))
            term = x[k] * exp_term
            summation += term
        result = round(summation.real, 4) / N
        x_n.append(result)

    SignalSamplesAreEqual('C:/Users/DELL/OneDrive/Desktop/Collage Courses/DSP/DSP_tasks/task4_test_cases/DFT/input_Signal_DFT.txt', indexes, x_n)
    return indexes, x_n

# C:/Users/DELL/OneDrive/Desktop/Collage Courses/DSP/DSP_tasks/task4_test_cases/DFT/input_Signal_DFT.txt

# C:/Users/DELL/OneDrive/Desktop/Collage Courses/DSP/DSP_tasks/task4_test_cases/IDFT/Input_Signal_IDFT_A,Phase.txt


##################################################################################################
#                                             Task 5                                             #
##################################################################################################
def dct(signal_path, save_nlines):
    signal_path = signal_path.get()
    save_nlines = int(save_nlines.get())
    x, y = read_samples(signal_path)
    complex_list = []
    N = len(y)
    for k in range(N):
        Yk = 0
        for n in range(N):
            Yk += y[n] * math.cos((math.pi / (4 * N)) * ((2 * n) - 1) * (2 * k - 1))
        Yk *= np.sqrt(2 / N)
        complex_list.append(Yk)
    x = [0] * N
    SignalSamplesAreEqual(r'C:\Users\DELL\OneDrive\Desktop\Collage Courses\DSP\DSP_tasks\task_5_files\DCT\DCT_output.txt', x, complex_list)
    save_task5_to_txt('saved_dct.txt', x, complex_list, save_nlines)

# C:\Users\DELL\OneDrive\Desktop\Collage Courses\DSP\DSP_tasks\task_5_files\DCT\DCT_input.txt
def removeDC(signal_path):
    signal_path = signal_path.get()
    X, Y = read_samples(signal_path)
    mean = np.mean(Y)
    complex_list = [round(y - mean, 3) for y in Y]
    SignalSamplesAreEqual(r'C:\Users\DELL\OneDrive\Desktop\Collage Courses\DSP\DSP_tasks\task_5_files\Remove DC component\DC_component_output.txt', X, complex_list)

# C:\Users\DELL\OneDrive\Desktop\Collage Courses\DSP\DSP_tasks\task_5_files\Remove DC component\DC_component_input.txt
def save_task5_to_txt(filename, amplitude, phase, m):
    with open(filename, 'w') as file:
        file.write(f"{0}\n")
        file.write(f"{1}\n")
        file.write(f"{len(amplitude)}\n")
        for i, (a, p) in enumerate(zip(amplitude, phase)):
            if i < m:
                file.write(f"{a:.0f},{p:.14f}\n")


##################################################################################################

win = Tk()
win.geometry("500x800")


# region TASK 4 VARIABLES
menu_op = StringVar()
signal_path = StringVar()
Fs = StringVar()
new_amp = StringVar()
new_phase = StringVar()
component_num = StringVar()
save_nlines = StringVar()
# endregion


# region TASK 4 WIDGETS

def fourier_transform(signal_path, Fs):
    signal_path = signal_path.get()
    Fs = float(Fs.get())
    x_k = dft(signal_path)
    amps, phases = get_amp_phase(x_k)
    sketch_dft(amps, phases, Fs)
    a, p = read_samples('C:/Users/DELL/OneDrive/Desktop/Collage Courses/DSP/DSP_tasks/task4_test_cases/DFT/Output_Signal_DFT_A,Phase.txt')
    amp2 = []
    for i in range(len(p)):
        p[i] = round(p[i], 8)
    for i in range(len(a)):
        a[i] = round(a[i], 13)
    for i in a:
        amp2.append(round(i, 13))
    print(SignalComapreAmplitude(a, amp2))
    print(SignalComapreAmplitude(p, phases))
    creat_signal_file(amps, phases)
    return amps, phases

def save_ft(amps, phases):
    pass


def reconstruct_idft(signal_path, Fs, component_num, new_amp, new_phase):
    if type(Fs) == 'StringVar':
        Fs = float(Fs.get())

    if type(signal_path) == 'StringVar':
        signal_path = signal_path.get()
    amps, phases = fourier_transform(signal_path, Fs)
    component_num = int(component_num.get())

    if new_amp.get() != "" and new_phase.get() != "":
        new_amp = float(new_amp.get())
        new_phase = float(new_phase.get())
        amps[component_num - 1] = new_amp
        phases[component_num - 1] = new_phase

    elif new_amp.get() != "":
        new_amp = float(new_amp.get())
        amps[component_num - 1] = new_amp

    elif new_phase.get() != "":
        new_phase = float(new_phase.get())
        phases[component_num - 1] = new_phase


    creat_signal_file(amps, phases)

    indexes, x_n = idft('./task_4_saved_signals/created_signal.txt')
    plot_discrete(indexes, x_n, 'Reconstructed IDFT')
    plt.show()


def read_ft(signal_path):
    signal_path = signal_path.get()
    indexes, x_n = idft(signal_path)
    plot_discrete(indexes, x_n, 'IDFT')
    plt.show()

def update_selected_option(*args):
    toggle_widgets_visibility(menu_op.get())


def toggle_widgets_visibility(op):
    if op == 'Construct FT':
        transform_button.place(x=230, y=200)
        # save_button.place(x=235, y=250)
    else:
        transform_button.place_forget()
        # save_button.place_forget()

    if op == 'Modify Amp & Phase':
        comp_label.place(x=120, y=200)
        comp_entry.place(x=260, y=200)
        amp_label.place(x=120, y=250)
        amp_entry.place(x=260, y=250)
        phase_label.place(x=120, y=300)
        phase_entry.place(x=260, y=300)
        # save_button.place(x=230, y=400)
        reconstruct_button.place(x=205, y=350)
    else:
        comp_label.place_forget()
        comp_entry.place_forget()
        amp_label.place_forget()
        amp_entry.place_forget()
        phase_label.place_forget()
        phase_entry.place_forget()
        reconstruct_button.place_forget()

    if op == 'Construct IDFT':
        read_button.place(x=230, y=200)
    else:
        read_button.place_forget()

    if op == 'Construct DCT':
        read_dct_button.place(x=230, y=200)
        save_nlines_label.place(x=120, y=150)
        save_nlines_entry.place(x=260, y=150)
        fs_label.place_forget()
        fs_entry.place_forget()
    else:
        read_dct_button.place_forget()
        save_nlines_label.place_forget()
        save_nlines_entry.place_forget()
        fs_label.place(x=120, y=150)
        fs_entry.place(x=260, y=150)

    if op == 'Remove DC':
        remove_dc_button.place(x=230, y=200)
        fs_label.place_forget()
        fs_entry.place_forget()
    else:
        remove_dc_button.place_forget()
        fs_label.place(x=120, y=150)
        fs_entry.place(x=260, y=150)


op_label = Label(win, text='Frequency Domain:')
op_label.place(x=120, y=50)
op_options = ['Construct FT', 'Modify Amp & Phase', 'Construct IDFT', 'Construct DCT', 'Remove DC']
op_dropMenu = OptionMenu(win, menu_op, *op_options, command=update_selected_option)
op_dropMenu.place(x=260, y=45)

path_label = Label(win, text='Signal Path:')
path_label.place(x=120, y=100)
path_entry = Entry(win, textvariable=signal_path)
path_entry.place(x=260, y=100)

fs_label = Label(win, text='Sampling Frequency:')
fs_label.place(x=120, y=150)
fs_entry = Entry(win, textvariable=Fs)
fs_entry.place(x=260, y=150)

transform_button = Button(win, text='Transform', command=partial(fourier_transform, signal_path, Fs), activeforeground='red')

# save_button = Button(win, text='Save FT', command=partial(save_ft, amps, phases), activeforeground='red')

comp_label = Label(win, text='Component Number:')
comp_entry = Entry(win, textvariable=component_num)

amp_label = Label(win, text='New Amplitude:')
amp_entry = Entry(win, textvariable=new_amp)

phase_label = Label(win, text='New Phase:')
phase_entry = Entry(win, textvariable=new_phase)

save_nlines_label = Label(win, text='Save nLines:')
save_nlines_entry = Entry(win, textvariable=save_nlines)

reconstruct_button = Button(win, text='Reconstruct IDFT', command=partial(reconstruct_idft, signal_path, Fs, component_num, new_amp, new_phase), activeforeground='red')

read_button = Button(win, text='Read FT', command=partial(read_ft, signal_path), activeforeground='red')

read_dct_button = Button(win, text='Read DCT', command=partial(dct, signal_path, save_nlines), activeforeground='red')

remove_dc_button = Button(win, text='Remove DC', command=partial(removeDC, signal_path), activeforeground='red')

# endregion


win.mainloop()

